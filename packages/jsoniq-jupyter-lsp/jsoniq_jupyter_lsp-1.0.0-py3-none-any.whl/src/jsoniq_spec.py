def load(app):
    return {
        "jsoniq_language_server": {
            "version": 2,
            "argv": ["jsoniq_lsp_start"],
            # Adding python is needed for the LSP extention to start the LS.
            "languages": ["jsoniq", "python"],
            "mime_types": [
                "application/jsoniq",
                "text/jsoniq",
                "text/x-jsoniq",
                "text/python",
                "text/x-python",
            ],
            "display_name": "JSONiq Language Server",
        }
    }
