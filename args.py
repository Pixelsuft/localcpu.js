import sys
import updater
import sock


NEED_UPDATE = False
AUTO_RUN_NODE = True


for i, arg in enumerate(sys.argv[1:]):
    lowered = arg.lower().strip()
    if lowered == '-u' or lowered == '--update':
        NEED_UPDATE = True
        continue
    if lowered == '-n' or lowered == '--no-autorun':
        AUTO_RUN_NODE = False
        continue
    if lowered == '-h' or lowered == '--host':
        sock.set_host(sys.argv[i + 1].strip())
        continue
    if lowered == '-p' or lowered == '--port':
        sock.set_host(int(sys.argv[i + 1].strip().lower()))
        continue


updater.update(NEED_UPDATE)
