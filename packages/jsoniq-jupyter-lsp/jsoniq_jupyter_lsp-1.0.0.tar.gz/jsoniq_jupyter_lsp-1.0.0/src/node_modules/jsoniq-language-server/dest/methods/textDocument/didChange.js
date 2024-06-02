import { documents, } from "../../documents.js";
import { diagnoseDocument } from "../diagnostics/diagnostic.js";
export const didChange = (message) => {
    const params = message.params;
    documents.set(params.textDocument.uri, params.contentChanges[0].text);
    // Document changes must result in a document diagnose as new content arrived.
    diagnoseDocument(params.textDocument.uri);
};
//# sourceMappingURL=didChange.js.map