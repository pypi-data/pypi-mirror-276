import { documents } from "../../documents.js";
import { diagnoseDocument } from "../diagnostics/diagnostic.js";
export const didOpen = (message) => {
    const params = message.params;
    documents.set(params.textDocument.uri, params.textDocument.text);
    // Document changes must result in a document diagnose as new content arrived.
    diagnoseDocument(params.textDocument.uri);
};
//# sourceMappingURL=didOpen.js.map