import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace the Login UI
old_login_portal_regex = re.compile(r'<!-- Login Portal Overlay -->.*?<!-- Script to demonstrate the interaction requested -->', re.DOTALL)

new_login_portal = """<!-- Login Portal Overlay -->
<div id="login-portal" class="fixed inset-0 bg-[#0a0e14]/95 backdrop-blur-md z-[200] flex flex-col items-center justify-center p-6 hidden">
    <div class="max-w-2xl w-full bg-surface-container-low border border-[#31353c]/30 shadow-[0_0_50px_rgba(0,0,0,0.8)] relative flex flex-col md:flex-row">
        
        <!-- Login Form -->
        <div class="w-full p-12 relative flex flex-col justify-center text-center items-center">
            <div class="absolute top-0 left-0 w-full h-1 bg-primary-container"></div>
            
            <div class="w-20 h-20 bg-surface border border-[#31353c]/50 rounded-full flex items-center justify-center mb-6">
                <img src="https://www.google.com/images/branding/googleg/1x/googleg_standard_color_128dp.png" alt="Google" class="w-10 h-10 opacity-80 backdrop-grayscale grayscale">
            </div>

            <h2 class="text-3xl font-black font-headline uppercase tracking-tighter mb-2 text-[#c8c6c5]">Operator Authentication</h2>
            <p class="font-body text-[10px] uppercase tracking-widest opacity-50 mb-8 pb-4">Secure OAuth 2.0 Identity Verification Required.</p>
            
            <button id="oauth-login-btn" onclick="window.location.href='/login/google'" class="w-full max-w-sm bg-white text-black flex items-center justify-center gap-4 py-4 font-black Inter uppercase tracking-tighter hover:bg-opacity-90 transition-all mt-4">
                <img src="https://www.google.com/images/branding/googleg/1x/googleg_standard_color_128dp.png" alt="Google" class="w-5 h-5">
                Sign in with Google
            </button>
            
            <div class="mt-8 text-[9px] uppercase tracking-widest font-bold opacity-30">
                <span class="material-symbols-outlined text-[12px] inline align-text-bottom mr-1">security</span> Read-only access requested. We do not store your emails.
            </div>
        </div>
    </div>
</div>

<!-- Script to demonstrate the interaction requested -->"""

html = old_login_portal_regex.sub(new_login_portal, html)

# 2. Update the JavaScript
old_js_regex = re.compile(r'// 2\. Login Portal -> Dashboard.*?</script>', re.DOTALL)

new_js = """// 2. Authentication Check on Load
        document.addEventListener('DOMContentLoaded', async () => {
            try {
                // To support both local testing and Render production cleanly
                const apiBase = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' 
                    ? '' 
                    : 'https://threatlevel-backend.onrender.com';
                    
                const res = await fetch(`${apiBase}/auth_status`);
                const data = await res.json();
                
                if (data.authenticated) {
                    // Start directly in Dashboard!
                    loginPortal.classList.add('hidden');
                    landingPage.classList.add('hidden');
                    dashboardApp.classList.remove('hidden');
                    
                    // Update Operator Name
                    const operatorNameEls = document.querySelectorAll('.operator-name-display');
                    operatorNameEls.forEach(el => el.textContent = data.email);
                    
                    // Auto-sync
                    syncBtn.click();
                }
            } catch (err) {
                console.log("Auth check skipped", err);
            }
        });

        // 3. Scan Inbox Action (OAuth Integration)
        syncBtn.addEventListener('click', async () => {
            overlay.classList.remove('hidden');
            
            try {
                const apiBase = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' 
                    ? '' 
                    : 'https://threatlevel-backend.onrender.com';
                    
                // Use GET request, NO payload! The backend uses the secure session token!
                const res = await fetch(`${apiBase}/scan_inbox`, {
                    method: 'GET'
                });
                const data = await res.json();
                
                if (data.data) {
                    tbody.innerHTML = ''; // Clear default hardcoded rows
                    
                    data.data.forEach(item => {
                        const tr = document.createElement('tr');
                        const isPhishing = item.prediction === 'phishing';
                        
                        tr.className = isPhishing 
                            ? "bg-surface border-b border-[#31353c]/10 hover:bg-surface-container-high transition-colors"
                            : "bg-surface-container-low border-b border-[#31353c]/10 hover:bg-surface-container-high transition-colors";
                            
                        const badgeHtml = isPhishing
                            ? `<span class="inline-flex items-center gap-2 border-l-2 border-[#990000] px-3 py-1 bg-primary-container/10 text-primary-fixed font-bold tracking-tight">PHISHING DETECTED</span>`
                            : `<span class="inline-flex items-center gap-2 border-l-2 border-[#77dc7a] px-3 py-1 bg-secondary-container/10 text-secondary font-bold tracking-tight">CLEAN</span>`;
                            
                        const colorClass = isPhishing ? 'text-primary' : 'text-secondary';
                        const snippetClass = isPhishing ? 'text-tertiary opacity-50 italic' : 'text-tertiary opacity-50';
                        
                        tr.innerHTML = `
                            <td class="px-6 py-5">${badgeHtml}</td>
                            <td class="px-6 py-5 font-mono ${colorClass} opacity-90">${item.sender.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</td>
                            <td class="px-6 py-5 font-bold uppercase tracking-tight">${item.subject.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</td>
                            <td class="px-6 py-5 ${snippetClass}">"${item.snippet.replace(/</g, '&lt;').replace(/>/g, '&gt;')}"</td>
                            <td class="px-6 py-5 text-right opacity-40 font-mono">LIVE</td>
                        `;
                        tbody.appendChild(tr);
                    });
                } else if(data.error) {
                    alert('Backend Authorization Error: ' + data.error);
                } else {
                    alert('Error from API: ' + JSON.stringify(data));
                }
            } catch (err) {
                alert('Connection to backend failed. Make sure backend is awake! ' + err);
            } finally {
                overlay.classList.add('hidden');
            }
        });
        
        // Setup Logout functionality
        document.querySelectorAll('a:contains("Logout") , button:contains("Terminate")').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.preventDefault();
                await fetch('/logout');
                window.location.reload();
            });
        });
        
        // polyfill for :contains
        HTMLElement.prototype.containsText = function(text) {
             return this.innerText.indexOf(text) > -1;
        };
        document.querySelectorAll('a, button').forEach(el => {
            if(el.innerText && el.innerText.includes('Logout') || (el.innerText && el.innerText.includes('Terminate'))) {
                el.addEventListener('click', async (e) => {
                    e.preventDefault();
                    await fetch('/logout');
                    window.location.href = "/";
                });
            }
        });
    </script>"""

html = old_js_regex.sub(new_js, html)

# Inject operator class for name updates
html = html.replace('>OPERATOR_01<', ' class="operator-name-display">OPERATOR_01<')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("DOM Updated successfully!")
