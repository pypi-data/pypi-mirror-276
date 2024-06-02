import { tokenLegend } from "./semanticHighlighting/tokenLegend.js";
export const initialize = (message) => {
    return {
        capabilities: {
            textDocumentSync: 1,
            semanticTokensProvider: {
                legend: tokenLegend,
                range: true,
                full: { delta: false },
            },
            completionProvider: {},
        },
        serverInfo: {
            name: "jsoniq-language-server",
            version: "1.1.1",
        },
    };
};
//# sourceMappingURL=initialize.js.map