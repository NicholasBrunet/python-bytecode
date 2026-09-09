export class FileExplorer {
    constructor(containerId, initialFiles, onFileSwitch) {
        this.container = document.getElementById(containerId);
        this.files = initialFiles;
        this.onFileSwitch = onFileSwitch;
        this.activeFile = Object.keys(initialFiles)[0];
    }

    render() {
        if (!this.container) return;
        
        this.container.innerHTML = `
            <div style="padding: 10px 20px; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; color: #858585; border-bottom: 1px solid #3c3c3c;">
                Explorer: Workspace
            </div>
            <ul style="padding: 10px; list-style: none; margin: 0;" id="explorer-file-list"></ul>
        `;

        const list = this.container.querySelector("#explorer-file-list");
        
        Object.keys(this.files).forEach(fileName => {
            const li = document.createElement("li");
            li.style.cssText = "padding: 6px 10px; border-radius: 4px; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 8px; margin-bottom: 2px;";
            li.className = fileName === this.activeFile ? "file-item active" : "file-item";
            li.innerHTML = `🐍 ${fileName}`;
            
            li.addEventListener("click", () => {
                if (this.activeFile === fileName) return;
                
                this.container.querySelectorAll("li").forEach(el => el.classList.remove("active"));
                li.classList.add("active");
                
                this.activeFile = fileName;
                this.onFileSwitch(fileName);
            });
            list.appendChild(li);
        });
    }
}
