import sys

import generate_notes
import git_push
import prepare_kit

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        raise "informe o nome do kit!"

    kit_name = args[1]

    generate_notes.run()
    prepare_kit.run(kit_name)
    git_push.run()
