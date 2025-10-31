#!/bin/bash

# Run by the user from the project root directory to set up the initial directory structure for conversion.
set -e

# The directory of this`` script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# OLD:
#mkdir -p tlv/conversion
#cd tlv/conversion
#cp -r "$SCRIPT_DIR"/project_setup_starting_instructions.md project_setup_instructions.md
#cp -r "$SCRIPT_DIR"/Dockerfile .
#chmod -w -R Dockerfile
#cp -r "$SCRIPT_DIR"/docker-compose.yml .
#p -r "$SCRIPT_DIR"/install_verilator .
#cp -r "$SCRIPT_DIR"/settings.local.json .
#cp -r "$SCRIPT_DIR"/claude-config.json .
#echo "✅ Conversion setup completed in tlv/conversion/"

# NEW:
mkdir -p tlv/regress
cp -r "$SCRIPT_DIR"/env tlv
cp -r "$SCRIPT_DIR"/instructions tlv/project_instructions
chmod -w -R tlv/env/Dockerfile
echo "✅ Baseline conversion setup complete, producing tlv/env/*, tlv/instructions/*, and empty tlv/regress/."
