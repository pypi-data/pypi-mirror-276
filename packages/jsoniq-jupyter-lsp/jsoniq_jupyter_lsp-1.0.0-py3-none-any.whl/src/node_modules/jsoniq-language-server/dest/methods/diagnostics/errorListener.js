export class DiagnosticErrorListener {
    constructor(items) {
        this._items = items;
    }
    get items() {
        return this._items;
    }
    syntaxError(recognizer, offendingSymbol, line, charPositionInLine, msg, e) {
        let tokenLength = 0;
        if (offendingSymbol) {
            tokenLength = offendingSymbol.text?.length ?? 0;
        }
        const diagnostic = {
            severity: 1,
            message: msg,
            range: {
                start: { line: line - 1, character: charPositionInLine },
                end: { line: line - 1, character: charPositionInLine + tokenLength },
            },
            source: "JSONiq language server",
        };
        this._items.push(diagnostic);
    }
}
//# sourceMappingURL=errorListener.js.map