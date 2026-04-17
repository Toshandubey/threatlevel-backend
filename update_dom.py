import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Header Links
html = html.replace(
    '<a class="text-secondary border-b-2 border-secondary pb-1 Inter uppercase font-black tracking-tighter text-sm" href="#">Dashboard</a>',
    '<a class="nav-btn active text-secondary border-b-2 border-secondary pb-1 Inter uppercase font-black tracking-tighter text-sm" href="#" data-target="view-dashboard">Dashboard</a>'
)
html = html.replace(
    '<a class="text-[#c8c6c5] opacity-50 hover:bg-[#31353c] transition-colors duration-150 Inter uppercase font-black tracking-tighter text-sm" href="#">Analytics</a>',
    '<a class="nav-btn text-[#c8c6c5] opacity-50 hover:opacity-100 hover:bg-[#31353c] transition-colors duration-150 Inter uppercase font-black tracking-tighter text-sm" href="#" data-target="view-analytics">Analytics</a>'
)
html = html.replace(
    '<a class="text-[#c8c6c5] opacity-50 hover:bg-[#31353c] transition-colors duration-150 Inter uppercase font-black tracking-tighter text-sm" href="#">Logs</a>',
    '<a class="nav-btn text-[#c8c6c5] opacity-50 hover:opacity-100 hover:bg-[#31353c] transition-colors duration-150 Inter uppercase font-black tracking-tighter text-sm" href="#" data-target="view-logs">Logs</a>'
)

# Header Icons
html = html.replace(
    '<button class="p-2 hover:bg-[#31353c] transition-colors duration-150">',
    '<button class="nav-btn p-2 hover:bg-[#31353c] transition-colors duration-150 opacity-50 hover:opacity-100" data-target="view-settings">'
, 1) # Only first one for settings

html = html.replace(
    '<button class="p-2 hover:bg-[#31353c] transition-colors duration-150">\n<span class="material-symbols-outlined text-tertiary">account_circle</span>\n</button>',
    '<button class="nav-btn p-2 hover:bg-[#31353c] transition-colors duration-150 opacity-50 hover:opacity-100" data-target="view-profile">\n<span class="material-symbols-outlined text-tertiary">account_circle</span>\n</button>'
)

# 2. Update Sidebar Links
html = html.replace(
    '<a class="flex items-center gap-4 px-6 py-4 bg-[#31353c] text-[#77dc7a] border-l-4 border-[#77dc7a] transition-all duration-75 ease-in" href="#">\n<span class="material-symbols-outlined" style="font-variation-settings: \'FILL\' 1;">mail</span>\n<span class="text-[11px] uppercase tracking-widest font-bold font-body">Primary Feed</span>\n</a>',
    '<a class="nav-btn active flex items-center gap-4 px-6 py-4 bg-[#31353c] text-[#77dc7a] border-l-4 border-[#77dc7a] transition-all duration-75 ease-in" href="#" data-target="view-dashboard">\n<span class="material-symbols-outlined" style="font-variation-settings: \'FILL\' 1;">mail</span>\n<span class="text-[11px] uppercase tracking-widest font-bold font-body">Primary Feed</span>\n</a>'
)
html = html.replace(
    '<a class="flex items-center gap-4 px-6 py-4 text-[#c8c6c5] opacity-40 hover:opacity-100 hover:bg-[#10141a] transition-all duration-75 ease-in" href="#">\n<span class="material-symbols-outlined">gpp_bad</span>\n<span class="text-[11px] uppercase tracking-widest font-bold font-body">Threat Vault</span>\n</a>',
    '<a class="nav-btn flex items-center gap-4 px-6 py-4 text-[#c8c6c5] opacity-40 hover:opacity-100 hover:bg-[#10141a] transition-all duration-75 ease-in" href="#" data-target="view-threatvault">\n<span class="material-symbols-outlined">gpp_bad</span>\n<span class="text-[11px] uppercase tracking-widest font-bold font-body">Threat Vault</span>\n</a>'
)
html = html.replace(
    '<a class="flex items-center gap-4 px-6 py-4 text-[#c8c6c5] opacity-40 hover:opacity-100 hover:bg-[#10141a] transition-all duration-75 ease-in" href="#">\n<span class="material-symbols-outlined">hub</span>\n<span class="text-[11px] uppercase tracking-widest font-bold font-body">Network Map</span>\n</a>',
    '<a class="nav-btn flex items-center gap-4 px-6 py-4 text-[#c8c6c5] opacity-40 hover:opacity-100 hover:bg-[#10141a] transition-all duration-75 ease-in" href="#" data-target="view-networkmap">\n<span class="material-symbols-outlined">hub</span>\n<span class="text-[11px] uppercase tracking-widest font-bold font-body">Network Map</span>\n</a>'
)
html = html.replace(
    '<a class="flex items-center gap-4 px-6 py-4 text-[#c8c6c5] opacity-40 hover:opacity-100 hover:bg-[#10141a] transition-all duration-75 ease-in" href="#">\n<span class="material-symbols-outlined">terminal</span>\n<span class="text-[11px] uppercase tracking-widest font-bold font-body">System Health</span>\n</a>',
    '<a class="nav-btn flex items-center gap-4 px-6 py-4 text-[#c8c6c5] opacity-40 hover:opacity-100 hover:bg-[#10141a] transition-all duration-75 ease-in" href="#" data-target="view-systemhealth">\n<span class="material-symbols-outlined">terminal</span>\n<span class="text-[11px] uppercase tracking-widest font-bold font-body">System Health</span>\n</a>'
)


# 3. Restructure the Main container
main_start = '<main class="md:ml-64 pt-24 pb-20 min-h-screen">'
if main_start in html:
    new_main = main_start + '\n<div id="view-dashboard" class="spa-view block">'
    html = html.replace(main_start, new_main)
else:
    print("Main start not found!")

main_end = '</main>'
new_end_views = """</div> <!-- End view-dashboard -->

<!-- THREAT VAULT VEW -->
<div id="view-threatvault" class="spa-view hidden max-w-7xl mx-auto p-8">
    <div class="mb-12 border-b border-[#31353c]/30 pb-8">
        <h2 class="text-4xl font-black Inter uppercase tracking-tighter mb-2 text-primary">Threat Vault</h2>
        <p class="text-tertiary opacity-60 font-body text-sm max-w-xl">Deep storage for confirmed malicious payloads, separated by attack vector and heuristic classification.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Mock Threat 1 -->
        <div class="bg-surface-container-low border border-[#990000]/30 p-6 flex flex-col gap-4 hover:bg-surface transition-colors cursor-pointer group">
            <div class="flex justify-between items-center">
                <span class="text-[#990000] font-black text-[10px] uppercase tracking-widest bg-primary-container/20 px-2 py-1">SPEAR PHISHING</span>
                <span class="text-tertiary opacity-40 text-xs font-mono">0xA491</span>
            </div>
            <h3 class="text-lg font-bold">"Urgent: Invoice Overdue"</h3>
            <p class="font-mono text-xs opacity-50 break-words">finance@paypal-support-verify.com</p>
            <div class="w-full bg-[#31353c] h-1 mt-auto">
                <div class="bg-[#990000] h-1 w-[98%]"></div>
            </div>
            <span class="text-[9px] uppercase tracking-widest opacity-30 mt-2">CONFIDENCE: 98.4%</span>
        </div>
        <!-- Mock Threat 2 -->
        <div class="bg-surface-container-low border border-secondary/30 p-6 flex flex-col gap-4 hover:bg-surface transition-colors cursor-pointer group">
            <div class="flex justify-between items-center">
                <span class="text-secondary font-black text-[10px] uppercase tracking-widest bg-secondary-container/20 px-2 py-1">SOCIAL ENGINEERING</span>
                <span class="text-tertiary opacity-40 text-xs font-mono">0xB122</span>
            </div>
            <h3 class="text-lg font-bold">"HR: Updated Time Off Policy"</h3>
            <p class="font-mono text-xs opacity-50 break-words">hr-internal@company-portal.net</p>
            <div class="w-full bg-[#31353c] h-1 mt-auto">
                <div class="bg-secondary h-1 w-[89%]"></div>
            </div>
            <span class="text-[9px] uppercase tracking-widest opacity-30 mt-2">CONFIDENCE: 89.1%</span>
        </div>
        <!-- Mock Threat 3 -->
        <div class="bg-surface-container-low border border-primary/30 p-6 flex flex-col gap-4 hover:bg-surface transition-colors cursor-pointer group">
            <div class="flex justify-between items-center">
                <span class="text-primary font-black text-[10px] uppercase tracking-widest bg-primary-container/20 px-2 py-1">MALWARE DROPPER</span>
                <span class="text-tertiary opacity-40 text-xs font-mono">0xC883</span>
            </div>
            <h3 class="text-lg font-bold">"Encrypted Document Attached"</h3>
            <p class="font-mono text-xs opacity-50 break-words">noreply@docusign-secure.com</p>
            <div class="w-full bg-[#31353c] h-1 mt-auto">
                <div class="bg-primary h-1 w-[99%]"></div>
            </div>
            <span class="text-[9px] uppercase tracking-widest opacity-30 mt-2">CONFIDENCE: 99.9%</span>
        </div>
    </div>
</div>

<!-- NETWORK MAP VIEW -->
<div id="view-networkmap" class="spa-view hidden max-w-7xl mx-auto p-8 h-[80vh] flex flex-col">
    <div class="mb-8 border-b border-[#31353c]/30 pb-4">
        <h2 class="text-4xl font-black Inter uppercase tracking-tighter mb-2">Network Origin Map</h2>
        <p class="text-tertiary opacity-60 font-body text-sm">Real-time geographical visualization of inbound SMTP traffic anomalies.</p>
    </div>
    <div class="flex-1 bg-[#05070a] border border-[#31353c]/50 relative overflow-hidden flex items-center justify-center">
        <!-- Decorative Grid overlay -->
        <div class="absolute inset-0 z-0 opacity-10" style="background-image: linear-gradient(#31353c 1px, transparent 1px), linear-gradient(90deg, #31353c 1px, transparent 1px); background-size: 40px 40px;"></div>
        
        <div class="relative z-10 w-full max-w-4xl opacity-40">
            <svg viewBox="0 0 1000 500" class="w-full h-full fill-[#31353c]">
                <!-- Very rudimentary mock world map nodes -->
                <circle cx="200" cy="150" r="4" class="animate-pulse fill-primary" />
                <circle cx="250" cy="200" r="3" />
                <circle cx="450" cy="100" r="5" class="animate-pulse fill-secondary" />
                <circle cx="500" cy="180" r="2" />
                <circle cx="700" cy="140" r="6" class="animate-pulse fill-primary" />
                <circle cx="800" cy="250" r="3" />
                
                <!-- Mock Connection Lines -->
                <path d="M 200 150 Q 325 100 450 100" stroke="#990000" stroke-width="1" fill="none" class="opacity-50" stroke-dasharray="4 4"/>
                <path d="M 700 140 Q 575 160 450 100" stroke="#77dc7a" stroke-width="1" fill="none" class="opacity-50"/>
            </svg>
        </div>
        
        <div class="absolute top-6 right-6 bg-[#10141a] p-4 text-[10px] font-mono border border-[#31353c]">
            <p class="text-primary mb-2">● HIGH RISK ORIGINS</p>
            <ul class="opacity-50 space-y-1">
                <li>104.28.19.44 (RU)</li>
                <li>45.144.225.19 (KP)</li>
                <li>192.168.1.1 (INT)</li>
            </ul>
        </div>
    </div>
</div>

<!-- SYSTEM HEALTH VIEW -->
<div id="view-systemhealth" class="spa-view hidden max-w-7xl mx-auto p-8">
    <div class="mb-12 border-b border-[#31353c]/30 pb-8">
        <h2 class="text-4xl font-black Inter uppercase tracking-tighter mb-2">System Health</h2>
        <p class="text-tertiary opacity-60 font-body text-sm">Hardware utilization and model inference metrics.</p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- CPU usage -->
        <div class="bg-surface-container-low p-8 border border-[#31353c]/20">
            <h4 class="text-[10px] uppercase font-bold tracking-widest text-secondary mb-6">Neural Engine CPU Load</h4>
            <div class="flex items-end gap-2 mb-2">
                <span class="text-5xl font-black">42</span><span class="text-secondary">%</span>
            </div>
            <div class="w-full bg-[#10141a] h-2">
                <div class="bg-secondary h-full w-[42%]"></div>
            </div>
        </div>
        
        <!-- RAM usage -->
        <div class="bg-surface-container-low p-8 border border-[#31353c]/20">
            <h4 class="text-[10px] uppercase font-bold tracking-widest text-[#c8c6c5] mb-6">Vector Memory (RAM)</h4>
            <div class="flex items-end gap-2 mb-2">
                <span class="text-5xl font-black">1.2</span><span class="opacity-50">GB / 4.0 GB</span>
            </div>
            <div class="w-full bg-[#10141a] h-2">
                <div class="bg-[#c8c6c5] h-full w-[30%]"></div>
            </div>
        </div>
        
        <!-- Inference Time -->
        <div class="bg-surface-container-low p-8 border border-[#31353c]/20">
            <h4 class="text-[10px] uppercase font-bold tracking-widest text-primary mb-6">Avg Inference Latency</h4>
            <div class="flex items-end gap-2 mb-2">
                <span class="text-5xl font-black">14.2</span><span class="text-primary">ms</span>
            </div>
            <!-- Mock Bar Chart -->
            <div class="flex items-end gap-1 h-12 mt-4 opacity-50">
                <div class="w-full bg-primary h-[40%]"></div>
                <div class="w-full bg-primary h-[35%]"></div>
                <div class="w-full bg-primary h-[45%]"></div>
                <div class="w-full bg-primary h-[80%]"></div>
                <div class="w-full bg-primary h-[30%]"></div>
                <div class="w-full bg-primary h-[40%]"></div>
                <div class="w-full bg-primary h-[20%]"></div>
            </div>
        </div>
        
        <!-- API Traffic -->
        <div class="bg-surface-container-low p-8 border border-[#31353c]/20 flex flex-col justify-center items-center text-center">
            <span class="material-symbols-outlined text-4xl text-[#77dc7a] mb-4">cloud_done</span>
            <p class="text-sm font-bold uppercase tracking-widest">Render Cloud Servers Secure</p>
            <p class="text-[10px] opacity-40 mt-2 uppercase">Uptime: 99.9% (Last 30 Days)</p>
        </div>
    </div>
</div>

<!-- ANALYTICS VIEW -->
<div id="view-analytics" class="spa-view hidden max-w-7xl mx-auto p-8">
    <div class="mb-12 border-b border-[#31353c]/30 pb-8 flex justify-between items-end">
        <div>
            <h2 class="text-4xl font-black Inter uppercase tracking-tighter mb-2">Threat Analytics</h2>
            <p class="text-tertiary opacity-60 font-body text-sm">Macroscopic review of classification outcomes.</p>
        </div>
        <button class="bg-[#31353c] px-4 py-2 text-[10px] uppercase font-bold tracking-widest">Last 30 Days</button>
    </div>
    
    <div class="grid grid-cols-3 gap-6 mb-8">
        <div class="bg-surface p-6 border-l-4 border-primary">
            <p class="text-[10px] uppercase opacity-50 font-bold tracking-widest">Total Scanned</p>
            <p class="text-3xl font-black mt-2">12,492</p>
        </div>
        <div class="bg-surface p-6 border-l-4 border-[#990000]">
            <p class="text-[10px] uppercase opacity-50 font-bold tracking-widest">Phishing Blocked</p>
            <p class="text-3xl font-black mt-2">4,129 <span class="text-[10px] opacity-40 ml-2">33%</span></p>
        </div>
        <div class="bg-surface p-6 border-l-4 border-secondary">
            <p class="text-[10px] uppercase opacity-50 font-bold tracking-widest">False Positive Rate</p>
            <p class="text-3xl font-black mt-2">0.06%</p>
        </div>
    </div>
</div>

<!-- LOGS VIEW -->
<div id="view-logs" class="spa-view hidden max-w-7xl mx-auto p-8 h-[80vh] flex flex-col">
    <div class="mb-6 border-b border-[#31353c]/30 pb-4">
        <h2 class="text-4xl font-black Inter uppercase tracking-tighter mb-2">System Logs</h2>
    </div>
    <div class="flex-1 bg-[#0a0e14] border border-[#31353c] p-6 overflow-y-auto font-mono text-xs space-y-2">
        <div class="flex gap-4"><span class="text-[#c8c6c5] opacity-40">[08:42:11]</span><span class="text-[#77dc7a]">INFO</span><span class="opacity-80">Gunicorn worker initialized</span></div>
        <div class="flex gap-4"><span class="text-[#c8c6c5] opacity-40">[08:42:12]</span><span class="text-[#77dc7a]">INFO</span><span class="opacity-80">Loading vectorizer.pkl...</span></div>
        <div class="flex gap-4"><span class="text-[#c8c6c5] opacity-40">[08:42:13]</span><span class="text-[#77dc7a]">INFO</span><span class="opacity-80">Loading final_model.pkl...</span></div>
        <div class="flex gap-4"><span class="text-[#c8c6c5] opacity-40">[08:42:14]</span><span class="text-[#77dc7a]">INFO</span><span class="opacity-80">Models loaded successfully. Pipeline ready.</span></div>
        <div class="flex gap-4"><span class="text-[#c8c6c5] opacity-40">[09:15:01]</span><span class="text-secondary">WARN</span><span class="opacity-80">POST /scan_inbox - Request received from operator</span></div>
        <div class="flex gap-4"><span class="text-[#c8c6c5] opacity-40">[09:15:02]</span><span class="text-[#77dc7a]">INFO</span><span class="opacity-80">IMAP connection established to imap.gmail.com</span></div>
        <div class="flex gap-4"><span class="text-[#c8c6c5] opacity-40">[09:15:04]</span><span class="text-[#77dc7a]">INFO</span><span class="opacity-80">Processed 10 recent emails. 2 Critical Threats identified.</span></div>
        <div class="flex gap-4"><span class="text-[#c8c6c5] opacity-40">[09:15:05]</span><span class="text-[#77dc7a]">INFO</span><span class="opacity-80">Payload delivered successfully (200 OK)</span></div>
        <!-- Blinking cursor -->
        <div class="w-2 h-4 bg-[#c8c6c5] animate-pulse mt-4"></div>
    </div>
</div>

<!-- PROFILE VIEW -->
<div id="view-profile" class="spa-view hidden max-w-3xl mx-auto p-8">
    <div class="mb-12 border-b border-[#31353c]/30 pb-8 grid place-items-center text-center">
        <div class="w-24 h-24 bg-surface-container-highest flex items-center justify-center rounded-full mb-6 border-2 border-secondary">
            <span class="material-symbols-outlined text-4xl text-secondary">account_circle</span>
        </div>
        <h2 class="text-4xl font-black Inter uppercase tracking-tighter mb-2">OPERATOR_01</h2>
        <span class="bg-[#31353c] px-3 py-1 text-[10px] uppercase tracking-widest font-bold">Clearance Level 4</span>
    </div>
    
    <div class="space-y-6">
        <div class="bg-surface p-6 border border-[#31353c]/30">
            <label class="block text-[10px] uppercase opacity-50 mb-2">Assigned Agent Name</label>
            <input type="text" value="OPERATOR_01" class="w-full bg-[#10141a] p-3 text-sm font-mono border border-[#31353c] focus:outline-none" disabled>
        </div>
        <div class="bg-surface p-6 border border-[#31353c]/30">
            <label class="block text-[10px] uppercase opacity-50 mb-2">Connected Target Inbox</label>
            <input type="text" value="[Encrypted In-Memory Token]" class="w-full bg-[#10141a] p-3 text-sm font-mono border border-[#31353c] text-secondary focus:outline-none" disabled>
        </div>
        <button class="w-full border border-primary text-primary py-4 hover:bg-primary hover:text-on-primary font-bold uppercase tracking-widest transition-colors text-xs">
            Terminate Session (Logout)
        </button>
    </div>
</div>

<!-- SETTINGS VIEW -->
<div id="view-settings" class="spa-view hidden max-w-4xl mx-auto p-8">
    <div class="mb-12 border-b border-[#31353c]/30 pb-8">
        <h2 class="text-4xl font-black Inter uppercase tracking-tighter mb-2">Core Settings</h2>
        <p class="text-tertiary opacity-60 font-body text-sm">Adjust machine learning parameters and interface preferences.</p>
    </div>
    
    <div class="space-y-6">
        <div class="flex items-center justify-between bg-surface-container-low p-6 border border-[#31353c]/20">
            <div>
                <h4 class="font-bold uppercase tracking-widest text-sm mb-1">Aggressive Heuristics</h4>
                <p class="text-[10px] opacity-50 font-body">Lowers the confidence threshold required to flag an email. Increases false positives.</p>
            </div>
            <div class="w-12 h-6 bg-[#31353c] rounded-full relative cursor-pointer group">
                <div class="w-6 h-6 bg-secondary absolute right-0 rounded-full group-hover:scale-110 transition-transform"></div>
            </div>
        </div>
        
        <div class="flex items-center justify-between bg-surface-container-low p-6 border border-[#31353c]/20">
            <div>
                <h4 class="font-bold uppercase tracking-widest text-sm mb-1">Visual Threat Indicators</h4>
                <p class="text-[10px] opacity-50 font-body">Enables high-contrast crimson colors for positive AI predictions.</p>
            </div>
            <div class="w-12 h-6 bg-[#31353c] rounded-full relative cursor-pointer group">
                <div class="w-6 h-6 bg-secondary absolute right-0 rounded-full group-hover:scale-110 transition-transform"></div>
            </div>
        </div>
        
        <div class="flex items-center justify-between bg-surface-container-low p-6 border border-[#31353c]/20">
            <div>
                <h4 class="font-bold uppercase tracking-widest text-sm mb-1">Store Local Scan History</h4>
                <p class="text-[10px] opacity-50 font-body">Cache JSON responses locally in the browser to view Analytics without re-scanning.</p>
            </div>
            <div class="w-12 h-6 bg-[#31353c] rounded-full relative cursor-pointer">
                <div class="w-6 h-6 bg-[#c8c6c5] opacity-30 absolute left-0 rounded-full"></div>
            </div>
        </div>
    </div>
</div>

</main>"""

html = html.replace(main_end, new_end_views)

# 4. Inject View Manager Script inside the JS block
js_start = "// 1. Landing Page -> Login Portal"
js_insertion = """// SPA View Manager
        const navBtns = document.querySelectorAll('.nav-btn');
        const spaViews = document.querySelectorAll('.spa-view');
        
        navBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Prevent default anchor jumping
                if(btn.tagName === 'A') e.preventDefault();
                
                const targetId = btn.getAttribute('data-target');
                if(!targetId) return;
                
                // 1. Hide all views
                spaViews.forEach(view => {
                    view.classList.add('hidden');
                    view.classList.remove('block');
                });
                
                // 2. Show target view
                const targetView = document.getElementById(targetId);
                if(targetView) {
                    targetView.classList.remove('hidden');
                    targetView.classList.add('block');
                }
                
                // 3. Update active states on Sidebar/Nav links
                // Reset all
                navBtns.forEach(b => {
                    if (b.classList.contains('border-l-4')) {
                        b.classList.remove('bg-[#31353c]', 'text-[#77dc7a]', 'border-[#77dc7a]');
                        b.classList.add('text-[#c8c6c5]', 'opacity-40');
                    } else if (b.classList.contains('border-b-2')) {
                        // Header links
                        b.classList.remove('border-b-2', 'border-secondary', 'text-secondary', 'pb-1');
                        b.classList.add('text-[#c8c6c5]', 'opacity-50');
                    }
                });
                
                // Set active (only for sidebar/header texts, not icons)
                if (btn.classList.contains('border-l-4') || btn.querySelector('.material-symbols-outlined')) {
                    // Sidebar
                    btn.classList.remove('text-[#c8c6c5]', 'opacity-40');
                    btn.classList.add('bg-[#31353c]', 'text-[#77dc7a]', 'border-[#77dc7a]');
                } else if (btn.tagName === 'A') {
                    // Header Nav
                    btn.classList.remove('text-[#c8c6c5]', 'opacity-50');
                    btn.classList.add('border-b-2', 'border-secondary', 'text-secondary', 'pb-1');
                }
            });
        });
        
        // 1. Landing Page -> Login Portal"""

html = html.replace(js_start, js_insertion)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("DOM Updated successfully!")
