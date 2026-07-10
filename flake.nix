{
  description = "micropython development environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    {
      self,
      nixpkgs,
      ...
    }:
    let
      systems = nixpkgs.lib.platforms.unix;
      eachSystem =
        f:
        nixpkgs.lib.genAttrs systems (
          system:
          f (
            import nixpkgs {
              inherit system;
              config = { };
              overlays = [ ];
            }
          )
        );

      mkLuna =
        {
          zlib,
          stdenv,
          fetchFromGitHub,
        }:
        stdenv.mkDerivation {
          version = "2.1";
          pname = "luna";
          src = fetchFromGitHub {
            owner = "ndless-nspire";
            repo = "Luna";
            rev = "a9924a9a968954eba9adcc161a58ac607f97ce8c";
            hash = "sha256-x/s3drSa0TC81SM+V7/WeQusDyY37OwToe+nEYyfdxA=";
          };
          installPhase = ''
            make install PREFIX="$out/bin"
          '';
          nativeBuildInputs = [ zlib ];
        };
      mkTns =
        {
          lib,
          bash,
          stdenv,
          coreutils,
          callPackage,
          luna ? null,
        }:
        let
          fs = lib.fileset;
          root = ./.;
          luna' = if luna == null then callPackage mkLuna { } else luna;
        in
        derivation {
          inherit (stdenv.hostPlatform) system;
          name = "digcod-tns";
          builder = "${bash}/bin/bash";
          src = fs.toSource {
            inherit root;
            fileset = fs.intersection (fs.gitTracked root) (
              fs.fileFilter (f: f.hasExt "py" && (!lib.hasPrefix "test" f.name)) root
            );
          };
          PATH = "$PATH:${coreutils}/bin";
          args = [
            "-c"
            ''ls "$src/"*.py | sort && mkdir -p "$out" && ${luna'}/bin/luna $(ls "$src/"*.py | sort) "$out/DigiCod_Nspire.tns"''
          ];
        };
    in
    {
      devShells = eachSystem (pkgs: {
        default = pkgs.mkShellNoCC {
          packages = with pkgs; [
            micropython
            self.packages.${pkgs.stdenv.hostPlatform.system}.luna
          ];
        };
      });

      overlays.default = _: _: {
        luna = mkLuna;
        digcod-tns = mkTns;
      };

      packages = eachSystem (
        pkgs:
        let
          luna = pkgs.callPackage mkLuna { };
          digcod-tns = pkgs.callPackage mkTns { };
        in
        {
          inherit luna digcod-tns;
          default = luna;
        }
      );

      apps = eachSystem (
        pkgs:
        (pkgs.lib.mapAttrs (_: drv: {
          type = "app";
          program = "${drv}${drv.passthru.exePath or "/bin/${drv.pname or drv.name}"}";
        }) self.packages.${pkgs.stdenv.hostPlatform.system})
        // {
          test =
            let
              mp = pkgs.lib.getExe pkgs.micropython;
              py = pkgs.lib.getExe pkgs.python3;
            in
            {
              type = "app";
              program = "${pkgs.writeShellScriptBin "test" ''
                echo "running test_unit.py" && 
                ${mp} test_unit.py && 
                echo "OK" && 
                echo "running test_interaction.py" && 
                ${py} test_interaction.py ${mp} && 
                echo "OK"
            ''}/bin/test";
            };
        }
      );
    };
}
