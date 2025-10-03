{ pkgs, ... }:

let
  pythonPackages = ps: with ps; [
    fastapi
    uvicorn
    psycopg2
    sqlalchemy
    pydantic
    passlib
    python-jose
    python-dotenv
  ];

  pythonWithPackages = pkgs.python3.withPackages pythonPackages;

in
{
  channel = "stable-24.05";
  
  # Volvemos a la configuración más simple posible.
  # Solo los paquetes que necesitamos, nada de automatización.
  packages = [
    pythonWithPackages
    pkgs.postgresql
    pkgs.docker
    pkgs.docker-compose
    pkgs.nodejs
  ]; 

  idx = {
    extensions = [
      "ms-python.python"
      "google.gemini-cli-vscode-ide-companion"
    ];
  };
}
