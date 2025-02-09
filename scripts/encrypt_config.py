import sys
from pathlib import Path

# Añadir el directorio raíz al PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from backend.app.utils.crypto import ConfigEncryption

def main():
    # Asegurarse de que existe el directorio config
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)

    crypto = ConfigEncryption()
    
    # Encriptar el archivo de configuración
    input_file = "config/config.yml"
    output_file = "config/config.yml.encrypted"
    
    crypto.encrypt_file(input_file, output_file)
    print(f"Configuración encriptada guardada en {output_file}")

if __name__ == "__main__":
    main()