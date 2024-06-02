import { clearPendingDiagnostic, documentsDiagnostics, } from "../diagnostics/diagnostic.js";
export const didClose = (message) => {
    const params = message.params;
    // Remove diagnostics on close
    documentsDiagnostics.delete(params.textDocument.uri);
    clearPendingDiagnostic(params.textDocument.uri);
};
//# sourceMappingURL=didClose.js.map