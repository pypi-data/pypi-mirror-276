import * as fs from "fs";
const log = fs.createWriteStream("/tmp/jsoniq-lsp.log");
export default {
    write: (message) => {
        // Only write if verbosity enabled
        if (true) {
            if (typeof message === "object") {
                log.write(JSON.stringify(message));
            }
            else {
                log.write(message);
            }
            log.write("\n");
        }
    },
};
//# sourceMappingURL=log.js.map