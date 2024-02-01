{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.poetry
    pkgs.poppler_utils
    pkgs.pdftk
    pkgs.glow
    pkgs.pandoc
  ];

  shellHook = ''
    echo "Entering nix-shell"
  '';
}
