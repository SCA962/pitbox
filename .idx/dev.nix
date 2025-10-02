{ pkgs, ... }: {
  channel = "stable-24.05";
  packages = [
    pkgs.python3
    pkgs.pip
    pkgs.postgresql
  ];
  idx = {
    extensions = [
      "ms-python.python"
      "google.gemini-cli-vscode-ide-companion"
    ];
  };
}