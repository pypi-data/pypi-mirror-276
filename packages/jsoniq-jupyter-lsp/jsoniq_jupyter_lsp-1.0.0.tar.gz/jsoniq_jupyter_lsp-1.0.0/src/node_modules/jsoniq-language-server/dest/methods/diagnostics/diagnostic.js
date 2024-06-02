import { connection } from "../../server.js";
import { documents } from "../../documents.js";
import { CharStreams, CommonTokenStream } from "antlr4ts";
import { jsoniqLexer } from "../../grammar/jsoniqLexer.js";
import { jsoniqParser } from "../../grammar/jsoniqParser.js";
import { DiagnosticErrorListener } from "./errorListener.js";
var DiagnosticSeverity;
(function (DiagnosticSeverity) {
    DiagnosticSeverity.Error = 1;
    DiagnosticSeverity.Warning = 2;
    DiagnosticSeverity.Information = 3;
    DiagnosticSeverity.Hint = 4;
})(DiagnosticSeverity || (DiagnosticSeverity = {}));
const pendingDocumentDiagnostics = new Map();
const DEFAULT_DELAY = 200; // 200ms delay before running diagnostics
export const documentsDiagnostics = new Map();
// @DEPRECATED
// Diagnostics are supported via push mechanism whenever clients support push diagnostics.
// export const diagnostic = (
//   message: RequestMessage
// ): FullDocumentDiagnosticReport | null => {
//   const params = message.params as DocumentDiagnosticParams;
//   const content = documents.get(params.textDocument.uri);
//   if (!content) {
//     return null;
//   }
//   const diagnostic = validateContent(content);
//   documentsDiagnostics.set(content, diagnostic);
//   return diagnostic;
// };
export const diagnoseDocument = (textDocumentUri) => {
    const content = documents.get(textDocumentUri);
    if (!content) {
        return null;
    }
    clearPendingDiagnostic(textDocumentUri);
    pendingDocumentDiagnostics.set(textDocumentUri, setTimeout(() => {
        // Remove self after delay expires
        pendingDocumentDiagnostics.delete(textDocumentUri);
        const diagnostic = validateContent(content);
        documentsDiagnostics.set(content, diagnostic);
        connection.sendDiagnostics({
            uri: textDocumentUri,
            diagnostics: diagnostic.items,
        });
    }, DEFAULT_DELAY));
};
export const validateContent = (content) => {
    const items = [];
    const inputStream = CharStreams.fromString(content);
    const lexer = new jsoniqLexer(inputStream);
    const tokenStream = new CommonTokenStream(lexer);
    const parser = new jsoniqParser(tokenStream);
    // Override error listener
    parser.removeErrorListeners();
    // Add our listener
    const diagnosticErrorListener = new DiagnosticErrorListener(items);
    parser.addErrorListener(diagnosticErrorListener);
    // Parse
    parser.moduleAndThisIsIt();
    return {
        kind: "full",
        items: diagnosticErrorListener.items,
    };
};
export const clearPendingDiagnostic = (textDocumentUri) => {
    const pendingDiagnostic = pendingDocumentDiagnostics.get(textDocumentUri);
    if (pendingDiagnostic) {
        clearTimeout(pendingDiagnostic);
        pendingDocumentDiagnostics.delete(textDocumentUri);
    }
};
//# sourceMappingURL=diagnostic.js.map