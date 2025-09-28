{
  description = "Web-based Mahjong game by faraplay";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ self, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } (
      { config, withSystem, ... }: {

        systems = [
          "x86_64-linux" "aarch64-darwin"
        ];

        perSystem = { pkgs, ... }: {

          devShells.default = pkgs.mkShell {
            packages = [ pkgs.nodejs_22 pkgs.python313 ];
          };

          packages = {

            zundamahjong-client = pkgs.callPackage (
              { lib, buildNpmPackage }:

              buildNpmPackage {
                pname = "zundamahjong-client";
                version = "0.0.0";

                src = ./client;

                npmDepsHash = "sha256-cO4dS6yCRU6oyEtSJGckmmh1R93ppRCWX9djA5frDrk=";
                npmPackFlags = [ "--ignore-scripts" ];

                installPhase = ''
                  runHook preInstall
                  mkdir -p $out/zundamahjong && cp -r ../client_build/* $out/zundamahjong
                  runHook postInstall
                '';

                meta = {
                  description = "Web-based Mahjong game";
                  homepage = "https://github.com/faraplay/zundamahjong";
                  license = lib.licenses.mit;
                };
              }
            ) { };

            zundamahjong = pkgs.callPackage (
              { lib, python3Packages }:

              python3Packages.buildPythonPackage {
                pname = "zundamahjong";
                version = "0.0.0";
                format = "pyproject";

                src = ./.;

                build-system = with python3Packages; [
                  setuptools
                ];

                dependencies = with python3Packages; [
                  pydantic python-socketio
                ];

                pythonImportsCheck = [
                  "zundamahjong"
                ];

                nativeCheckInputs = with python3Packages; [
                  pytestCheckHook
                ];

                meta = {
                  description = "Web-based Mahjong game";
                  homepage = "https://github.com/faraplay/zundamahjong";
                  license = lib.licenses.mit;
                };
              }
            ) { };

          };

        };

        flake = {

          overlays.default = _: prev:
            withSystem prev.stdenv.hostPlatform.system ({ config, ... }: {
              inherit (config.packages) zundamahjong zundamahjong-client;
            });

          nixosModules.default =
            { config, lib, pkgs, ... }:

            let
              cfg = config.services.zundamahjong;

              pythonEnv = pkgs.python3.withPackages (ps: [
                ps.gunicorn cfg.server # Watch the Python version!
              ]);
            in

            {
              options = {

                services.zundamahjong = {

                  enable = lib.mkEnableOption "zundamahjong";

                  client = lib.mkPackageOption pkgs "zundamahjong-client" { };
                  server = lib.mkPackageOption pkgs "zundamahjong" { };

                  hostName = lib.mkOption {
                    type = lib.types.str;
                    description = "FQDN for the zundamahjong instance.";
                    default = "mahjong.${config.networking.domain}";
                  };

                };

              };

              config = lib.mkMerge [

                {
                  nixpkgs.overlays = [ self.overlays.default ];
                }

                (
                  lib.mkIf cfg.enable {

                    services.nginx.virtualHosts."${cfg.hostName}" = {

                      root = cfg.client;

                      locations."= /" = {
                        return = "301 /zundamahjong/";
                      };

                      locations."~ ^/socket.io/.*" = {
                        proxyPass = "http://unix:/run/zundamahjong/web.sock";
                        proxyWebsockets = true;
                      };

                    };

                    systemd.services.zundamahjong = {
                      wantedBy = [ "multi-user.target" ];
                      after = [ "network.target" ];

                      path = [ pythonEnv ];
                      script = ''
                        gunicorn --threads 8 --bind unix:///run/zundamahjong/web.sock zundamahjong.server:app
                      '';

                      serviceConfig = {
                        User = "zundamahjong";
                        Group = "zundamahjong";
                        DynamicUser = true;

                        RuntimeDirectory = "zundamahjong";
                        WorkingDirectory = "/var/lib/zundamahjong";
                        StateDirectory = "zundamahjong";
                      };
                    };

                  }
                )

              ];

            };

        };

      }
    );
}
