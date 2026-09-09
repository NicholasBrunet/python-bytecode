import { EditorState } from "@codemirror/state";
import { EditorView, hoverTooltip } from "@codemirror/view";
import { python } from "@codemirror/lang-python";
import { oneDark } from "@codemirror/theme-one-dark";
import { basicSetup } from "codemirror";

// Import your raw component models
import { FileExplorer } from "../components/FileExplorer";
import { TerminalPanel } from "../components/TerminalPanel";
import { StatusBar } from "../components/StatusBar";

const localFiles = {
    "main.py": `"""\nMain module for virtual execution mapping\n"""\nimport math\n\ndef run():\n    return math.sqrt(256)\n`,
    "utils.py": `"""\nHelper utilities for local operations\n"""\ndef format_log(msg):\n    return f"[LOG] {msg}"\n`
};

let activeFile = "main.py";
let editorView = null;
let docDatabase = { modules: {} }; // 📚 Holds your custom pvr-docs.json data

// Catch the custom security clearance event before drawing anything
document.addEventListener("pvr-auth-verified", (e) => {
    const verifiedToken = e.detail.token;
    console.log("PVR Core: Workspace security cleared. Loading panel components.");
    
    initializeWorkspaceWorkspace(verifiedToken);
});

async function initializeWorkspaceWorkspace(token) {
    // 1. Fetch your custom documentation JSON file asynchronously
    try {
        const res = await fetch("/pvr-docs.json");
        docDatabase = await res.json();
    } catch (err) {
        console.error("PVR IDE: Could not load pvr-docs.json configuration layouts:", err);
    }

    // 2. Build Hover Tooltip Extension Hook using your json definitions
    const pvrHoverProvider = hoverTooltip((view, pos, side) => {
        let { from, to } = view.state.doc.lineAt(pos);
        let lineText = view.state.doc.sliceString(from, to);
        
        let match = view.state.wordAt(pos);
        if (!match) return null;
        
        let startIdx = match.from - from;
        let endIdx = match.to - from;
        
        while (startIdx > 0 && lineText[startIdx - 1] === '.') {
            let prevWordStart = startIdx - 1;
            while (prevWordStart > 0 && /[\w]/.test(lineText[prevWordStart - 1])) {
                prevWordStart--;
            }
            startIdx = prevWordStart;
        }
        
        const fullTokenPath = lineText.slice(startIdx, endIdx);
        if (!fullTokenPath.includes(".")) return null;

        const [moduleKey, methodKey] = fullTokenPath.split(".");
        const targetMethod = docDatabase.modules[moduleKey]?.methods?.[methodKey];

        if (!targetMethod) return null;

        return {
            pos: startIdx + from,
            end: endIdx + from,
            above: true,
            create(view) {
                const dom = document.createElement("div");
                dom.style.padding = "8px 12px";
                dom.style.background = "#252526";
                dom.style.border = "1px solid #3c3c3c";
                dom.style.color = "#d4d4d4";
                dom.style.fontFamily = "sans-serif";
                dom.style.fontSize = "13px";
                dom.style.borderRadius = "4px";
                dom.style.boxShadow = "0 4px 12px rgba(0,0,0,0.4)";
                dom.style.maxWidth = "350px";
                dom.style.lineHeight = "1.5";

                dom.innerHTML = `
                    <div style="font-family:monospace;color:#4da6ff;font-weight:bold;margin-bottom:6px;">${targetMethod.signature}</div>
                    <div style="color:#aaaaaa;font-size:12px;">${targetMethod.doc}</div>
                `;
                return { dom };
            }
        };
    });

    // 3. Mount layout components into place
    const terminal = new TerminalPanel("terminal-panel-hook");
    terminal.render();

    const statusBar = new StatusBar("status-bar-hook");
    statusBar.render("Workspace Verified");

    const explorer = new FileExplorer("sidebar-explorer", localFiles, (switchedFile) => {
        // Handle file state switching safely
        localFiles[activeFile] = editorView.state.doc.toString();
        activeFile = switchedFile;
        
        editorView.setState(EditorState.create({
            doc: localFiles[activeFile],
            extensions: [basicSetup, python(), oneDark, pvrHoverProvider] // 🌟 Keep hover active on swap
        }));
        terminal.writeLog(`Switched file buffer target context to: ${switchedFile}`);
    });
    explorer.render();

    // 4. Initialize Core Editor with your hover extensions embedded
    editorView = new EditorView({
        state: EditorState.create({
            doc: localFiles[activeFile],
            extensions: [
                basicSetup,
                python(),
                oneDark,
                pvrHoverProvider // 🌟 Injects documentation cards natively on mouse hover
            ]
        }),
        parent: document.getElementById("editor")
    });
}
