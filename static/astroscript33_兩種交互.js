        
// 點擊主標題展開/收合子選單的邏輯
// function toggleSubmenu(id) {
//     const currentSubmenu = document.getElementById(id + '-submenu');
//     const currentArrow = document.getElementById(id + '-arrow');
    
//     // 取得所有子選單和箭頭
//     const allSubmenus = document.querySelectorAll('.submenu');
//     const allArrows = document.querySelectorAll('.main-item i'); // 假設箭頭都在 main-item 內

//     // 迴圈遍歷所有子選單
//     allSubmenus.forEach(submenu => {
//         // 如果子選單不是你當前點擊的，就把它隱藏
//         if (submenu.id !== currentSubmenu.id) {
//             submenu.classList.add('hidden');
//         }
//     });

//     // 迴圈遍歷所有箭頭
//     allArrows.forEach(arrow => {
//         // 如果箭頭不是你當前點擊的，就把它旋轉回來
//         if (arrow.id !== currentArrow.id) {
//             arrow.classList.remove('rotate-180');
//         }
//     });

//     // 最後，才對你當前點擊的選單進行切換
//     currentSubmenu.classList.toggle('hidden');
//     currentArrow.classList.toggle('rotate-180');
// }
        //* ai_astrology_guide.html 的原 script
        // 頁面切換功能
        function showSection(sectionId) {
            // 隱藏所有內容區塊
            const sections = document.querySelectorAll('.content-section');
            sections.forEach(section => {
                section.classList.remove('active');
            });
            
            // 隱藏 hero 區塊
            const hero = document.getElementById('hero');
            if (hero) {
                hero.style.display = 'none';
            }
            
            // 顯示目標區塊
            const targetSection = document.getElementById(sectionId);
            if (targetSection) {
                targetSection.classList.add('active');
            }
            
            // 關閉手機選單
            closeMobileMenu();
        }

        // // 初始化 - 顯示首頁
        // document.addEventListener('DOMContentLoaded', function() {
        //     // 預設顯示星盤資料生成頁面
        //     showSection('birth-chart');
        // });

        //* astro__格子版ok.html 的 原 script

        document.addEventListener('DOMContentLoaded', () => {
            console.log('Script Start Test! Version: Refactored v3.0');

            /*** 複製指定內容到剪貼簿。
                        * @param {string} textToCopy 要複製的文字。
                        * @param {HTMLElement} btnElement 觸發複製的按鈕元素 (可選)。
                        */
            function copyContent(textToCopy, btnElement) {
                if (!textToCopy || textToCopy.trim() === '') {
                    console.error("複製錯誤: 沒有內容可複製。");
                    if (btnElement) {
                        btnElement.textContent = '複製失敗';
                        setTimeout(() => btnElement.textContent = '複製', 2000);
                    }
                    return;
                }

                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(textToCopy.trim())
                        .then(() => {
                            if (btnElement) {
                                const originalText = btnElement.textContent;
                                btnElement.textContent = '已複製!';
                                setTimeout(() => {
                                    btnElement.textContent = originalText;
                                }, 2000);
                            }
                        })
                        .catch(err => {
                            console.error('複製到剪貼簿失敗，嘗試降級方案:', err);
                            fallbackCopyToClipboardSimple(textToCopy, btnElement);
                        });
                } else {
                    console.warn('瀏覽器不支持 navigator.clipboard，使用降級複製方案。');
                    fallbackCopyToClipboardSimple(textToCopy, btnElement);
                }
            }

            // 降級複製方案 (用於不支援 navigator.clipboard 的瀏覽器)
            function fallbackCopyToClipboardSimple(textToCopy, button) {
                const textarea = document.createElement('textarea');
                textarea.value = textToCopy.trim();
                textarea.style.position = 'fixed'; // 防止滾動
                textarea.style.opacity = 0; // 隱藏 textarea
                document.body.appendChild(textarea);
                textarea.focus();
                textarea.select();

                try {
                    document.execCommand('copy');
                    if (button) {
                        const originalText = button.textContent;
                        button.textContent = '已複製!';
                        setTimeout(() => {
                            button.textContent = originalText;
                        }, 2000);
                    }
                } catch (err) {
                    console.error('fallback 複製失敗: ', err);
                    alert('複製失敗，您的瀏覽器可能不支援自動複製功能。請手動複製。');
                    if (button) {
                        button.textContent = '複製失敗';
                        setTimeout(() => button.textContent = '複製', 2000);
                    }
                } finally {
                    textarea.remove(); // 移除臨時的 textarea
                }
            }
            // 【新增】為 AI 提問範例的複製按鈕設定事件監聽器
            document.body.addEventListener('click', function(event) {
                if (event.target.classList.contains('copy-prompt-btn')) {
                    const promptTextElement = event.target.previousElementSibling;
                    if (promptTextElement && promptTextElement.tagName === 'P') {
                        const textToCopy = promptTextElement.textContent;
                        // 直接複用我們強大的 copyContent 函式！
                        copyContent(textToCopy, event.target);
                    }
                }
            });

            // 定義一個全局變數來追蹤當前的顯示模式，預設為 'table'
            let currentDisplayMode = 'table'; // 可以是 'table' 或 'narrative'

            // 獲取切換按鈕的 DOM 元素
            const toggleTableModeBtn = document.getElementById('toggle-table-mode');
            const toggleNarrativeModeBtn = document.getElementById('toggle-narrative-mode');

            // 函數：更新顯示模式 (UI 和內容)
            function updateDisplayMode(newMode) {
                // 只有當模式確實改變時才更新全域狀態 (主要由按鈕點擊觸發)
                if (currentDisplayMode !== newMode) {
                    currentDisplayMode = newMode;
                }

                // 總是根據當前的狀態來更新 UI
                // 這確保了即使模式沒有改變 (例如重新計算後)，UI 也能被強制同步到正確的狀態
                const modeToShow = currentDisplayMode;

                if (toggleTableModeBtn) {
                    toggleTableModeBtn.classList.toggle('active', modeToShow === 'table');
                }
                if (toggleNarrativeModeBtn) {
                    toggleNarrativeModeBtn.classList.toggle('active', modeToShow === 'narrative');
                }

                const tableContents = document.querySelectorAll('.table-content');
                const narrativeContents = document.querySelectorAll('.narrative-content');

                tableContents.forEach(el => {
                    el.style.display = (modeToShow === 'table') ? 'block' : 'none';
                });

                narrativeContents.forEach(el => {
                    el.style.display = (modeToShow === 'narrative') ? 'block' : 'none';
                });
            }

        //    async function handleCopyButtonClick(event) {
        //         const button = event.currentTarget;
        //         let contentToCopy = ''; // 確保它一開始就是空字串

        //         try {
        //             if (button.classList.contains('copy-report-btn')) {
        //                 const reportWrapper = button.closest('.report-wrapper');
        //                 if (!reportWrapper) { // 加強檢查：如果找不到報告範圍，直接返回
        //                     alert('無法找到報告內容範圍。');
        //                     console.error('Copy report button clicked, but .report-wrapper not found.');
        //                     return;
        //                 }

        //                 const mainReportTitleElement = reportWrapper.querySelector('.report-main-header h2');
        //                 if (mainReportTitleElement) {
        //                     contentToCopy += mainReportTitleElement.textContent.trim() + '\n';
        //                 }

    
        //                 const chartWrappers = reportWrapper.querySelectorAll('.chart-wrapper');
        //                 chartWrappers.forEach(chartWrapper => {
        //                     const chartTitleElement = chartWrapper.querySelector('.chart-main-header h2');
        //                     if (chartTitleElement) {
        //                         contentToCopy += '\n' + chartTitleElement.textContent.trim() + '\n';
        //                         contentToCopy += '====================\n';
        //                     }

        //                     // 確保獲取的是文字內容，並處理找不到元素的情況
        //                      // 【核心修改】從整個 chartWrapper 改為只在 .sub-sections-container 中尋找，以排除 summary 區塊
        //                 const preElements = chartWrapper.querySelectorAll(`.sub-sections-container pre.${currentDisplayMode}-content, .sub-sections-container div.${currentDisplayMode}-content`);
                              
        //                 preElements.forEach(pre => {
        //                         if (pre) { // 確保 pre 存在
        //                             contentToCopy += pre.innerText.trim() + '\n\n'; // 使用 trim() 確保沒有多餘空白
        //                         }
        //                     });
        //                 });
        //                 contentToCopy = contentToCopy.trim(); // 最後再 trim 一次整個字串

        //             } else if (button.classList.contains('copy-chart-btn')) {
        //                 const chartWrapper = button.closest('.chart-wrapper');
        //                 if (!chartWrapper) { // 加強檢查：如果找不到命盤範圍，直接返回
        //                     alert('無法找到單一命盤內容範圍。');
        //                     console.error('Copy chart button clicked, but .chart-wrapper parent not found.');
        //                     return;
        //                 }

        //                 const chartTitleElement = chartWrapper.querySelector('.chart-main-header h2');
        //                 if (chartTitleElement) {
        //                     contentToCopy += chartTitleElement.textContent.trim() + '\n';
        //                     contentToCopy += '====================\n';
        //                 }

        //                 // 確保獲取的是文字內容，並處理找不到元素的情況
        //                 const preElements = chartWrapper.querySelectorAll(`.sub-sections-container pre.${currentDisplayMode}-content`);
        //                 preElements.forEach(pre => {
        //                     if (pre) { // 確保 pre 存在
        //                         contentToCopy += pre.innerText.trim() + '\n\n';
        //                     }
        //                 });
        //                 contentToCopy = contentToCopy.trim();

        //             } else if (button.classList.contains('section-copy-btn')) {
        //                 const sectionItem = button.closest('.result-section-item');
        //                 if (!sectionItem) { // 加強檢查：如果找不到區塊範圍，直接返回
        //                     alert('無法找到區塊內容範圍。');
        //                     console.error('Section copy button clicked, but .result-section-item parent not found.');
        //                     return;
        //                 }

        //                 // 這是最常見的出錯點，確保 preElement 存在且取得其 innerText
        //                 const preElement = sectionItem.querySelector(`pre.${currentDisplayMode}-content`);
        //                 if (preElement) { // <-- 關鍵檢查：確保 preElement 確實找到了
        //                     contentToCopy = preElement.innerText.trim(); // <-- 從元素中提取文字內容
        //                 } else {
        //                     contentToCopy = ''; // 如果找不到 <pre>，則內容為空字串，而不是 undefined 或 null
        //                     console.warn(`在 ${currentDisplayMode}-content 中沒有找到 <pre> 元素進行複製。`);
        //                 }
        //             }

        //             // 最後的檢查，確保 contentToCopy 是字串
        //             if (typeof contentToCopy !== 'string') {
        //                 console.error("錯誤：contentToCopy 最終不是字串，而是:", contentToCopy);
        //                 alert('複製內容格式錯誤。');
        //                 return;
        //             }

        //             if (contentToCopy === '') {
        //                 alert('沒有找到可複製的內容。');
        //                 return;
        //             }

        //             // 在這裡，contentToCopy 必須是字串
        //             await copyContent(contentToCopy, button);

        //         } catch (error) {
        //             console.error('複製內容時發生錯誤:', error);
        //             alert('複製失敗，請檢查控制台錯誤。');
        //             if (button) {
        //                 button.textContent = '複製失敗';
        //                 setTimeout(() => button.textContent = '複製', 2000);
        //             }
        //         }
        //     }
            // // 設置複製按鈕事件監聽器的函數
            // function setupCopyListeners() {
            //     // 移除舊的事件監聽器，避免重複綁定
            //     const oldCopyButtons = document.querySelectorAll('.copy-chart-btn, .section-copy-btn, .copy-report-btn');
            //     oldCopyButtons.forEach(button => {
            //         button.removeEventListener('click', handleCopyButtonClick);
            //     });

            //     // 重新綁定事件監聽器
            //     const copyButtons = document.querySelectorAll('.copy-chart-btn, .section-copy-btn, .copy-report-btn');
            //     console.log("setupCopyListeners: 找到的複製按鈕數量:", copyButtons.length);
            //     copyButtons.forEach(button => {
            //         button.addEventListener('click', handleCopyButtonClick);
            //     });
            // }

            

             // 設置複製按鈕事件監聽器的函數
            function setupCopyListeners() {
                // 移除舊的事件監聽器，避免重複綁定
                const oldCopyButtons = document.querySelectorAll('.copy-chart-btn, .section-copy-btn, .copy-report-btn, .download-report-btn, .download-chart-btn');
                oldCopyButtons.forEach(button => {
                    button.removeEventListener('click', handleCopyButtonClick);
                });

                // 重新綁定事件監聽器
                const copyButtons = document.querySelectorAll('.copy-chart-btn, .section-copy-btn, .copy-report-btn, .download-report-btn, .download-chart-btn');
                console.log("setupCopyListeners: 找到的複製按鈕數量:", copyButtons.length);
                copyButtons.forEach(button => {
                    button.addEventListener('click', handleCopyButtonClick);
                });
            }


            // 整合後的 handleCopyButtonClick 版本
            async function handleCopyButtonClick(event) {
    const button = event.currentTarget;
    let contentToCopy = ''; // 確保它一開始就是空字串

    try {
        // 合併複製報告和下載報告按鈕的邏輯
        if (button.classList.contains('copy-report-btn') || button.classList.contains('download-report-btn')) {
            const reportWrapper = button.closest('.report-wrapper');
            if (!reportWrapper) {
                alert('無法找到報告內容範圍。');
                console.error('Copy/Download report button clicked, but .report-wrapper not found.');
                return;
            }
            
            // 1. 先蒐集 Title
            const mainReportTitleElement = reportWrapper.querySelector('.report-main-header h2');
            if (mainReportTitleElement) {
                contentToCopy += mainReportTitleElement.textContent.trim() + '\n\n';
            }

            
            const chartWrappers = reportWrapper.querySelectorAll('.chart-wrapper');
    chartWrappers.forEach((chartWrapper, index) => { // 新增 index 參數
        // 先蒐集每個命盤各自的 Title
        const chartTitleElement = chartWrapper.querySelector('.chart-main-header h2');
        if (chartTitleElement) {
            if (index > 0) {
                contentToCopy += '\n\n\n'; // 在每個命盤之間增加額外空行
            }
            contentToCopy += '\n' + chartTitleElement.textContent.trim() + '\n';
            contentToCopy += '====================\n';
        }

        // 新增邏輯：如果按鈕是下載報告，則在 Title 後額外加入 summary 內容
        if (button.classList.contains('download-report-btn')) {
            // 在此範圍內尋找 table-content，確保它只屬於當前的 chartWrapper
            const summaryElement = chartWrapper.querySelector(`pre.table-content`);
            if (summaryElement) {
                contentToCopy += summaryElement.innerText.trim() + '\n\n';
            }
        }
        
        // 再蒐集其他除了 summary 以外的文字內容
        const preElements = chartWrapper.querySelectorAll(`.sub-sections-container pre.${currentDisplayMode}-content, .sub-sections-container div.${currentDisplayMode}-content`);
        preElements.forEach(pre => {
            if (pre) {
                contentToCopy += pre.innerText.trim() + '\n\n';
            }
        });
    });

    // 3. 最後蒐集所有互動區塊的內容
    const interactionContainer = reportWrapper.querySelector(':scope > .sub-sections-container');
    if (interactionContainer) {
        // 【新增】在互動區塊內容開始前，加入三個空行，但僅限於下載按鈕
        if (button.classList.contains('download-report-btn')) {
            contentToCopy += '\n\n\n';
        }

        const sectionItems = interactionContainer.querySelectorAll('.result-section-item');
        sectionItems.forEach(item => {
            const preElement = item.querySelector(`pre.${currentDisplayMode}-content`);
            if (preElement) {
                contentToCopy += preElement.innerText.trim() + '\n\n';
            }
        });
    }

    contentToCopy = contentToCopy.trim();
            
            // 處理「沒有找到內容」的警示
            if (contentToCopy === '') {
                alert('沒有找到可處理的內容。');
                return;
            }

            // 這裡根據按鈕的 class 決定是下載還是複製
            if (button.classList.contains('download-report-btn')) {

                // 取得 mainReportTitleElement 的文字作為檔名，並移除多餘空格
                let filename = mainReportTitleElement.textContent.trim();
    
                // 如果標題為空，則使用預設檔名
                if (filename === '') {
                    filename = '占星報告';
                }

                // 根據目前的顯示模式，新增後綴
                if (currentDisplayMode === 'table') {
                    filename += ' (表格式文字)';
                   } else if (currentDisplayMode === 'narrative') {
                      filename += ' (敘述模式)';
                }
    
            // 呼叫下載函式，並傳入新的動態檔名
            downloadTextFile(button, contentToCopy, filename + '.txt');
            } else {
                await copyContent(contentToCopy, button);
              }

            } else if (button.classList.contains('copy-chart-btn') || button.classList.contains('download-chart-btn')) {
               const chartWrapper = button.closest('.chart-wrapper');
                if (!chartWrapper) {
                alert('無法找到單一命盤內容範圍。');
                console.error('Copy chart button clicked, but .chart-wrapper parent not found.');
                return;
            }

            // 蒐集 單命盤的 Title
            const chartTitleElement = chartWrapper.querySelector('.chart-main-header h2');
            if (chartTitleElement) {
                contentToCopy += chartTitleElement.textContent.trim() + '\n';
                contentToCopy += '====================\n\n';
            }

            // 新增的邏輯：如果按鈕是下載按鈕，則額外加入 summary 內容
            if (button.classList.contains('download-chart-btn')) {
            const summaryElement = chartWrapper.querySelector(`pre.table-content`);
            console.log("找到的 summaryElement:", summaryElement); // <-- 新增這行

                if (summaryElement) {
                  console.log("summaryElement 的內容:", summaryElement.innerText); // <-- 新增這行
                  
                  // 【修正】這裡將 `=` 改為 `+=`，讓內容追加在最後面
                    contentToCopy += summaryElement.innerText.trim() + '\n\n';
                //   contentToCopy = summaryElement.innerText.trim() + '\n\n' + contentToCopy;
                }
            }

            // 再蒐集其他除了summary以外的文字內容
            const preElements = chartWrapper.querySelectorAll(`.sub-sections-container pre.${currentDisplayMode}-content`);
            preElements.forEach(pre => {
                if (pre) {
                    contentToCopy += pre.innerText.trim() + '\n\n';
                }
            });


            contentToCopy = contentToCopy.trim();
            
            if (contentToCopy === '') {
                alert('沒有找到可處理的內容。');
                return;
            }
            
            // 新增的邏輯：根據按鈕類別決定動作
            if (button.classList.contains('download-chart-btn')) {
                // 取得 chartTitleElement 的文字作為檔名，並移除多餘空格
                let filename = chartTitleElement.textContent.trim();

                // 如果標題為空，則使用預設檔名
                if (filename === '') {
                    filename = '單命盤報告';
                }

                // 根據目前的顯示模式，新增後綴
                if (currentDisplayMode === 'table') {
                      filename += ' (表格式文字)';
                  } else if (currentDisplayMode === 'narrative') {
                      filename += ' (敘述模式)';
                }
    

                // 呼叫下載函式，並傳入新的動態檔名
                downloadTextFile(button, contentToCopy, filename + '.txt');
            
            } else {
                await copyContent(contentToCopy, button);
            }
            
        } else if (button.classList.contains('section-copy-btn')) {
            const sectionItem = button.closest('.result-section-item');
            if (!sectionItem) {
                alert('無法找到區塊內容範圍。');
                console.error('Section copy button clicked, but .result-section-item parent not found.');
                return;
            }
            const preElement = sectionItem.querySelector(`pre.${currentDisplayMode}-content`);
            if (preElement) {
                contentToCopy = preElement.innerText.trim();
            } else {
                contentToCopy = '';
                console.warn(`在 ${currentDisplayMode}-content 中沒有找到 <pre> 元素進行複製。`);
            }
            if (contentToCopy === '') {
                alert('沒有找到可複製的內容。');
                return;
            }
            await copyContent(contentToCopy, button);
        }

    } catch (error) {
        console.error('處理按鈕事件時發生錯誤:', error);
        alert('操作失敗，請檢查控制台錯誤。');
        if (button) {
            button.textContent = '操作失敗';
            setTimeout(() => button.textContent = '複製', 2000);
        }
    }
}


            // async function handleCopyButtonClick(event) {
            //     const button = event.currentTarget;
            //     let contentToCopy = ''; // 確保它一開始就是空字串

            //     try {
            //         if (button.classList.contains('copy-report-btn')|| button.classList.contains('download-report-btn')) {
            //             const reportWrapper = button.closest('.report-wrapper');
            //             if (!reportWrapper) { // 加強檢查：如果找不到報告範圍，直接返回
            //                 alert('無法找到報告內容範圍。');
            //                 console.error('Copy report button clicked, but .report-wrapper not found.');
            //                 return;
            //             }

            //             const mainReportTitleElement = reportWrapper.querySelector('.report-main-header h2');
            //             if (mainReportTitleElement) {
            //                 contentToCopy += mainReportTitleElement.textContent.trim() + '\n';
            //             }

    
            //             const chartWrappers = reportWrapper.querySelectorAll('.chart-wrapper');
            //             chartWrappers.forEach(chartWrapper => {
            //                 const chartTitleElement = chartWrapper.querySelector('.chart-main-header h2');
            //                 if (chartTitleElement) {
            //                     contentToCopy += '\n' + chartTitleElement.textContent.trim() + '\n';
            //                     contentToCopy += '====================\n';
            //                 }

            //                 // 確保獲取的是文字內容，並處理找不到元素的情況
            //                  // 【核心修改】從整個 chartWrapper 改為只在 .sub-sections-container 中尋找，以排除 summary 區塊
            //             const preElements = chartWrapper.querySelectorAll(`.sub-sections-container pre.${currentDisplayMode}-content, .sub-sections-container div.${currentDisplayMode}-content`);
                              
            //             preElements.forEach(pre => {
            //                     if (pre) { // 確保 pre 存在
            //                         contentToCopy += pre.innerText.trim() + '\n\n'; // 使用 trim() 確保沒有多餘空白
            //                     }
            //                 });
            //             });

            //     // 【問題修正】為了解決合盤報告無法複製互動區塊（疊盤、交互相位）的問題，
            //     // 我們在此特別找出不在 .chart-wrapper 內的 .sub-sections-container，並複製其內容。
            //     // 這個容器通常包含了比較盤和行運盤的互動分析。
            //     const interactionContainer = reportWrapper.querySelector(':scope > .sub-sections-container');
            //     if (interactionContainer) {
            //         const sectionItems = interactionContainer.querySelectorAll('.result-section-item');
            //         sectionItems.forEach(item => {
            //             // 【使用者要求】只複製內文，不複製小標題
            //             const preElement = item.querySelector(`pre.${currentDisplayMode}-content`);
            //             if (preElement) {
            //                 contentToCopy += preElement.innerText.trim() + '\n\n';
            //             }
            //         });
            //     }

            //             contentToCopy = contentToCopy.trim(); // 最後再 trim 一次整個字串

            //         } else if (button.classList.contains('copy-chart-btn')) {
            //             const chartWrapper = button.closest('.chart-wrapper');
            //             if (!chartWrapper) { // 加強檢查：如果找不到命盤範圍，直接返回
            //                 alert('無法找到單一命盤內容範圍。');
            //                 console.error('Copy chart button clicked, but .chart-wrapper parent not found.');
            //                 return;
            //             }

            //             const chartTitleElement = chartWrapper.querySelector('.chart-main-header h2');
            //             if (chartTitleElement) {
            //                 contentToCopy += chartTitleElement.textContent.trim() + '\n';
            //                 contentToCopy += '====================\n';
            //             }

            //             // 確保獲取的是文字內容，並處理找不到元素的情況
            //             const preElements = chartWrapper.querySelectorAll(`.sub-sections-container pre.${currentDisplayMode}-content`);
            //             preElements.forEach(pre => {
            //                 if (pre) { // 確保 pre 存在
            //                     contentToCopy += pre.innerText.trim() + '\n\n';
            //                 }
            //             });
            //             contentToCopy = contentToCopy.trim();

            //         } else if (button.classList.contains('section-copy-btn')) {
            //             const sectionItem = button.closest('.result-section-item');
            //             if (!sectionItem) { // 加強檢查：如果找不到區塊範圍，直接返回
            //                 alert('無法找到區塊內容範圍。');
            //                 console.error('Section copy button clicked, but .result-section-item parent not found.');
            //                 return;
            //             }

            //             // 這是最常見的出錯點，確保 preElement 存在且取得其 innerText
            //             const preElement = sectionItem.querySelector(`pre.${currentDisplayMode}-content`);
            //             if (preElement) { // <-- 關鍵檢查：確保 preElement 確實找到了
            //                 contentToCopy = preElement.innerText.trim(); // <-- 從元素中提取文字內容
            //             } else {
            //                 contentToCopy = ''; // 如果找不到 <pre>，則內容為空字串，而不是 undefined 或 null
            //                 console.warn(`在 ${currentDisplayMode}-content 中沒有找到 <pre> 元素進行複製。`);
            //             }
            //         }

            //         // 最後的檢查，確保 contentToCopy 是字串
            //         if (typeof contentToCopy !== 'string') {
            //             console.error("錯誤：contentToCopy 最終不是字串，而是:", contentToCopy);
            //             alert('複製內容格式錯誤。');
            //             return;
            //         }

            //         // **從這裡開始替換您原本的 await copyContent 呼叫**
            //         // 新增的邏輯：根據按鈕類別決定動作
            //         if (button.classList.contains('download-report-btn')) {
            //         // 如果是下載按鈕，則呼叫下載函數
            //         downloadTextFile(contentToCopy, '占星報告.txt');
            //         } else {
            //         // 否則，執行原有的複製到剪貼簿功能
            //         await copyContent(contentToCopy, button);
            //         }


            //     } catch (error) {
            //         console.error('複製內容時發生錯誤:', error);
            //         alert('複製失敗，請檢查控制台錯誤。');
            //         if (button) {
            //             button.textContent = '複製失敗';
            //             setTimeout(() => button.textContent = '複製', 2000);
            //         }
            //     }
            // }

            // 為切換按鈕添加事件監聽器
            if (toggleTableModeBtn) {
                toggleTableModeBtn.addEventListener('click', () => updateDisplayMode('table'));
            }
            if (toggleNarrativeModeBtn) {
                toggleNarrativeModeBtn.addEventListener('click', () => updateDisplayMode('narrative'));
            }

            // 在你的網頁完全載入或生成報告後調用
            document.addEventListener('DOMContentLoaded', () => {
                // 預設將報告內容設為表格模式顯示
                updateDisplayMode('table');
                // 設置複製按鈕監聽器
                setupCopyListeners();
            });

            // 監聽 DOM 變動，如果內容是動態載入的，則需要重新設置監聽器
            const observer = new MutationObserver((mutationsList, observer) => {
                // 檢查是否有新的 .chart-wrapper 或 .result-section-item 被添加
                let shouldRescan = false;
                for (const mutation of mutationsList) {
                    if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                        for (const node of mutation.addedNodes) {
                            if (node.nodeType === 1 && (node.matches('.chart-wrapper') || node.matches('.result-section-item'))) {
                                shouldRescan = true;
                                break;
                            }
                        }
                    }
                    if (shouldRescan) break;
                }

                if (shouldRescan) {
                    console.log("DOM 結構變動，重新設置複製按鈕監聽器。");
                    setupCopyListeners(); // 正確呼叫修改後的函數名稱
                }
            });

            // 開始觀察 body 元素及其子元素的變化
            observer.observe(document.body, { childList: true, subtree: true });





            // *下載文字內容為 .txt 文件的函數*
            function downloadTextFile(buttonElement, content, filename) {
    // 確保按鈕元素存在，避免錯誤
    if (!buttonElement) return;

    // 創建 Blob 和 URL
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    // 創建並點擊 <a> 元素
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    // 在下載成功後，改變按鈕文字
    buttonElement.textContent = '已下載';

    // 設置計時器，在 2 秒後恢復文字
    setTimeout(() => {
        // 根據 class 判斷是哪個按鈕，並恢復其原始文字
        if (buttonElement.classList.contains('download-report-btn')) {
            buttonElement.textContent = '下載完整報告';
        } else if (buttonElement.classList.contains('download-chart-btn')) {
            buttonElement.textContent = '下載此盤';
        }
    }, 2000); // 2000 毫秒 = 2 秒
}
// function downloadTextFile(content, filename) {
//     // 創建一個 Blob 物件，類型為純文字
//     const blob = new Blob([content], { type: 'text/plain' });
    
//     // 創建一個臨時的 URL 來指向這個 Blob
//     const url = URL.createObjectURL(blob);
    
//     // 創建一個隱藏的 <a> 元素來觸發下載
//     const a = document.createElement('a');
//     a.href = url;
//     a.download = filename; // 設定下載時的檔案名稱
//     document.body.appendChild(a);
    
//     // 模擬點擊 <a> 元素來啟動下載
//     a.click();
    
//     // 清理資源，釋放創建的 URL
//     document.body.removeChild(a);
//     URL.revokeObjectURL(url);
// }

// 範例：如何在您的 handleCopyButtonClick 函數中調用它
// async function handleCopyButtonClick(event) {
//     const button = event.currentTarget;
//     let contentToCopy = ''; // 確保它一開始就是空字串

//     // ... (這裡保留您原有的邏輯，將所有內容組合成 contentToCopy 變數) ...
//     if (button.classList.contains('copy-report-btn')|| button.classList.contains('download-report-btn')) {
//         // ... (原有的複製程式碼邏輯) ...

//         contentToCopy = contentToCopy.trim();

//         if (contentToCopy === '') {
//             alert('沒有找到可複製的內容。');
//             return;
//         }

//         // === 在這裡新增呼叫下載函數 ===
//         // 假設您的下載按鈕有 .download-report-btn 這個 class
//         // 您可以根據按鈕的 class 來決定是複製還是下載
//         if (button.classList.contains('download-report-btn')) {
//             downloadTextFile(contentToCopy, '占星報告.txt');
//         } else {
//             // 原有的複製到剪貼簿功能
//             await copyContent(contentToCopy, button);
//         }
//     }
//     // ... (其他複製按鈕的邏輯) ...
// }


            // 如果你的報告是動態生成的，並且是在 DOMContentLoaded 之後才渲染，
            // 那麼你需要在報告渲染完成後，再次呼叫 updateDisplayMode('table');
            // 例如，在你呼叫 displayReport(reportHtmlContent); 之後：
            // displayReport(reportHtmlContent);
            // updateDisplayMode(currentDisplayMode); // 確保新生成的內容也符合當前模式
            // =============================================================
            // 全域設定與常數
            // =============================================================
            const BASE_API_URL = 'https://astro-chart-to-text.onrender.com/'; // 相對路徑，適用於前後端同源部署
            const YOUR_API_KEY = window.FRONTEND_ASTRO_API_KEY || "local_dev_key";
            const HOUSE_DEFINING_POINTS = ['上升', '下降', '天頂', '天底'];
            const DISPLAY_ORDER_NAMES = [
                "太陽", "月亮", "水星", "金星", "火星", "木星", "土星", "天王", "海王", "冥王",
                "凱龍", "穀神", "智神", "婚神", "灶神", "愛神", "莉莉絲", "靈神", "人龍",
                "北交", "南交", "上升", "下降", "天頂", "天底", "宿命", "福點"
            ];
            const commonTimezones = [
                "Asia/Taipei", "Asia/Shanghai", "Asia/Chongqing", "Asia/Tokyo", "Asia/Hong_Kong", "Asia/Singapore",
                "America/New_York", "America/Los_Angeles", "America/Chicago", "America/Denver",
                "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Rome",
                "Australia/Sydney", "Australia/Melbourne", "Australia/Perth"
            ];
            let allTimezones = [];

            // =============================================================
            // 工具函式
            // =============================================================

            // 轉換度數為度分格式
            function formatDegreesMinutesSeconds(decimalDegrees) {
                if (typeof decimalDegrees !== 'number' || isNaN(decimalDegrees)) return "N/A";
                let d = Math.floor(decimalDegrees);
                let minutesDecimal = (decimalDegrees - d) * 60;
                let m = Math.round(minutesDecimal);
                if (m >= 60) {
                    d += 1;
                    m = 0;
                }
                return `${String(d).padStart(2, '0')}°${String(m).padStart(2, '0')}'`;
            }

            // 顯示特定輸入框的錯誤
            function showInputError(inputId, message) {
                const inputElement = document.getElementById(inputId);
                const errorElement = document.getElementById(`${inputId}-error`);
                if (inputElement && errorElement) {
                    errorElement.textContent = message;
                    errorElement.style.display = 'block';
                    inputElement.style.setProperty('--input-border-color', '#ef4444');
                }
            }

            // 清除所有輸入框的錯誤
            function clearAllInputErrors() {
                document.querySelectorAll('.input-error-message').forEach(el => {
                    el.textContent = '';
                    el.style.display = 'none';
                });
                document.querySelectorAll('.input-field, .select-field').forEach(el => {
                    el.style.setProperty('--input-border-color', '#cbd5e0');
                });
            }

            // =============================================================
            // 初始化與事件監聽器設定
            // =============================================================

            // 頁面啟動時執行的主要函式
            async function initializeApp() {
                setupTabListeners();
                setupNavigation(); // 【新增】執行導覽列功能設定
                setupSubChartListeners();
                setupPlanetCheckboxes();
                setupInputErrorClearing();
                setupCustomTimezoneListeners();
                // setupWheelPickers(); // 【新增】啟用轉輪選擇器
                setDefaultTransitTimeToNow();// 【新增】為行運盤設定預設時間
                setDefaultSingleChartTimeToNow(); // 【新增】為個人盤設定預設時間


                document.getElementById('calculateBtn').addEventListener('click', calculateChart);

                updateMainTabVisibility('singleChartTab'); // 預設顯示個人盤
                updateSubChartVisibility('comparison');   // 預設雙人盤子選項為比較盤

                try {
                    // 不再使用全域時區列表和自動完成功能，簡化邏輯
                    populateTimezoneSelects();
                    console.log('時區下拉列表填充完成！');
                } catch (error) {
                    console.error('初始化時區功能失敗:', error);
                }
            }

            // =============================================================
            // 導覽列與選單功能 (Refactored)
            // =============================================================
            function setupNavigation() {
                const hamburger = document.getElementById('hamburger');
                const mobileMenu = document.getElementById('mobile-menu');
                const nav = document.querySelector('nav'); // 獲取整個 <nav> 元素

                if (!hamburger || !mobileMenu || !nav) {
                    console.warn('導覽列或漢堡選單元素未找到，功能將無法啟用。');
                    return;
                }

                // 統一的關閉選單函式
                function closeMenu() {
                    hamburger.classList.remove('active');
                    mobileMenu.classList.add('hidden');
                    document.body.classList.remove('overflow-hidden');
                }

                // 漢堡按鈕點擊事件
                hamburger.addEventListener('click', (event) => {
                    event.stopPropagation(); // 防止事件冒泡到 document
                    const isActive = hamburger.classList.toggle('active');
                    mobileMenu.classList.toggle('hidden');
                    document.body.classList.toggle('overflow-hidden', isActive);
                });

                // 【新增】點擊選單內的連結時，關閉選單
                mobileMenu.addEventListener('click', (event) => {
                    // 確保點擊的是一個 <a> 連結
                    if (event.target.tagName === 'A') {
                        closeMenu();
                    }
                });

                // 點擊選單外部區域關閉選單
                document.addEventListener('click', (event) => {
                    // 檢查點擊的目標是否在 <nav> 之外，並且選單是打開的
                    // !nav.contains(event.target) 確保點擊的不是導覽列本身
                    // !mobileMenu.classList.contains('hidden') 確保只在選單打開時作用
                    if (!nav.contains(event.target) && !mobileMenu.classList.contains('hidden')) {
                        closeMenu();
                    }
                });
            }

            // 4. 【新增】一個用來設定轉輪的全新函式
            function setupWheelPickers() {
                // 建立小時和分鐘的資料來源
                const hoursData = Array.from({ length: 24 }, (_, i) => String(i).padStart(2, '0'));
                const minutesData = Array.from({ length: 60 }, (_, i) => String(i).padStart(2, '0'));

                // 遍歷所有需要轉輪的輸入框
                const timeInputs = [
                    { id: 'single_hour', data: hoursData }, { id: 'single_minute', data: minutesData },
                    { id: 'comp1_hour', data: hoursData }, { id: 'comp1_minute', data: minutesData },
                    { id: 'comp2_hour', data: hoursData }, { id: 'comp2_minute', data: minutesData },
                    { id: 'natal_hour', data: hoursData }, { id: 'natal_minute', data: minutesData },
                    { id: 'transit_hour', data: hoursData }, { id: 'transit_minute', data: minutesData },
                ];

                timeInputs.forEach(inputConfig => {
                    const inputElement = document.getElementById(inputConfig.id);
                    if (inputElement) {
                        new Picker(inputElement, {
                            data: [inputConfig.data], // Picker.js 需要二維陣列
                            headers: false, // 不顯示標頭
                            format: 'HH:mm', // 這是 Picker.js 內部的格式，我們只用它來取值
                            text: { done: '確定', cancel: '取消' },
                            // 當使用者按下「確定」時，套件會自動將選擇的值更新到 inputElement.value
                        });
                    }
                });
            }

            // 【新增】這是一個全新的函式
            function setDefaultTransitTimeToNow() {
                const now = new Date();

                // 獲取並填入年、月、日、時、分
                document.getElementById('transit_year').value = now.getFullYear();
                document.getElementById('transit_month').value = now.getMonth() + 1; // getMonth() 是從 0 開始，所以要 +1
                document.getElementById('transit_day').value = now.getDate();
                document.getElementById('transit_hour').value = now.getHours();
                document.getElementById('transit_minute').value = now.getMinutes();
            }

             // 【新增】為個人盤設定預設時間
            function setDefaultSingleChartTimeToNow() {
                const now = new Date();

                // 獲取並填入年、月、日、時、分
                document.getElementById('single_year').value = now.getFullYear();
                document.getElementById('single_month').value = now.getMonth() + 1; // getMonth() 是從 0 開始，所以要 +1
                document.getElementById('single_day').value = now.getDate();
                document.getElementById('single_hour').value = now.getHours();
                document.getElementById('single_minute').value = now.getMinutes();
            }

            // 設定主頁籤切換
            function setupTabListeners() {
                document.querySelectorAll('.tab-button').forEach(button => {
                    button.addEventListener('click', (event) => {
                        updateMainTabVisibility(event.currentTarget.id);
                    });
                });
            }

            // 設定雙人盤的子選項切換
            function setupSubChartListeners() {
                document.querySelectorAll('.chart-card-sub').forEach(card => {
                    card.addEventListener('click', () => {
                        updateSubChartVisibility(card.dataset.chartType);
                    });
                });
            }


            // 優化的小行星/虛點選項 toggle
            function setupPlanetCheckboxes() {
    const optionalPlanetsConfig = {
        '核心星體': ["太陽", "月亮", "水星", "金星", "火星", "木星", "土星", "天王", "海王", "冥王"],
        '四軸': ["上升", "下降", "天頂", "天底"],
        '命運與潛意識': ["北交", "南交", "宿命", "福點", "莉莉絲"],
        '小行星': ["凱龍", "穀神", "智神", "婚神", "灶神", "愛神", "靈神", "人龍"]
    };
    const container = document.getElementById('optionalPlanetsContainer');
    container.innerHTML = ''; // 清空

    // 動態生成所有內容
    for (const groupName in optionalPlanetsConfig) {
        // 建立一個包含標題和按鈕的 header div
        const headerDiv = document.createElement('div');
        headerDiv.className = 'planet-group-header col-span-full mt-2';
        headerDiv.style.display = 'flex';
        headerDiv.style.justifyContent = 'space-between';
        headerDiv.style.alignItems = 'center';

        // 建立分類標題
        const groupTitle = document.createElement('span');
        groupTitle.className = 'font-semibold text-lg text-fuchsia-900';
        groupTitle.textContent = groupName;

        // 建立分類切換按鈕，並重新加回
        const groupToggleButton = document.createElement('button');
        groupToggleButton.className = 'planet-toggle-btn group-toggle-btn';
        groupToggleButton.textContent = '此類取消';
        groupToggleButton.dataset.state = 'all-checked';
        groupToggleButton.dataset.groupKey = groupName;

        headerDiv.appendChild(groupTitle);
        headerDiv.appendChild(groupToggleButton);
        container.appendChild(headerDiv);

        // 生成該分類下的所有 checkbox
        optionalPlanetsConfig[groupName].forEach(planet => {
            const wrapper = document.createElement('div');
            wrapper.className = 'flex items-center';
            wrapper.innerHTML = `
                <input id="chk-${planet}" type="checkbox" value="${planet}" class="optional-planet-checkbox h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" data-group="${groupName}" checked>
                <label for="chk-${planet}" class="ml-2 block text-lg text-gray-900">${planet}</label>
            `;
            container.appendChild(wrapper);
        });
    }

    // 使用「事件代理」來統一處理所有按鈕的點擊事件
    const selectionDiv = document.getElementById('planetSelection');
    selectionDiv.addEventListener('click', (event) => {
        const target = event.target;

        // --- 處理「總開關」按鈕 ---
        if (target.id === 'toggleAllPlanetsBtn') {
            event.stopPropagation(); // 阻止事件冒泡！
            const checkboxes = document.querySelectorAll('.optional-planet-checkbox');
            const isChecked = target.dataset.state === 'all-checked';
            checkboxes.forEach(cb => { cb.checked = !isChecked; });
            target.textContent = isChecked ? '全部選取' : '全部取消';
            target.dataset.state = isChecked ? 'all-unchecked' : 'all-checked';

            // 同步更新所有分類按鈕的狀態和文字
            document.querySelectorAll('.group-toggle-btn').forEach(btn => {
                btn.textContent = isChecked ? '此類別選取' : '此類取消';
                btn.dataset.state = isChecked ? 'all-unchecked' : 'all-checked';
            });
        }

        // --- 處理「分類」按鈕 ---
        if (target.classList.contains('group-toggle-btn')) {
            const groupKey = target.dataset.groupKey;
            const checkboxesInGroup = document.querySelectorAll(`.optional-planet-checkbox[data-group="${groupKey}"]`);
            const isChecked = target.dataset.state === 'all-checked';
            checkboxesInGroup.forEach(cb => { cb.checked = !isChecked; });
            target.textContent = isChecked ? '此類別選取' : '此類取消';
            target.dataset.state = isChecked ? 'all-unchecked' : 'all-checked';
        }
    });

    // 最後，確保最上面的總按鈕也套用新樣式
    // document.getElementById('toggleAllPlanetsBtn').className = 'planet-toggle-btn all-toggle-btn';
}

// 處理整個「顯示選項」區塊的開合
const toggleHeader = document.getElementById('toggleHeader');
const optionalPlanetsContainer = document.getElementById('optionalPlanetsContainer');
const toggleIcon = document.getElementById('toggleIcon');
const toggleAllPlanetsBtn = document.getElementById('toggleAllPlanetsBtn'); // 選擇「全部取消」按鈕

if (toggleHeader && optionalPlanetsContainer && toggleIcon && toggleAllPlanetsBtn) {
    toggleHeader.addEventListener('click', () => {
        // 如果目前是收合狀態 (有 hidden class)
        if (optionalPlanetsContainer.classList.contains('hidden')) {
            // 則展開面板、顯示按鈕，並旋轉箭頭
            optionalPlanetsContainer.classList.remove('hidden');
            toggleAllPlanetsBtn.classList.remove('hidden');
            toggleIcon.classList.add('rotate-90');
        } else {
            // 如果目前是展開狀態
            // 則收合面板、隱藏按鈕，並恢復箭頭
            optionalPlanetsContainer.classList.add('hidden');
            toggleAllPlanetsBtn.classList.add('hidden');
            toggleIcon.classList.remove('rotate-90');
        }
    });
}


            // 原本的 小行星/虛點選項
            // function setupPlanetCheckboxes() {
            //     const optionalPlanetsConfig = {
            //         '核心星體': ["太陽", "月亮", "水星", "金星", "火星", "木星", "土星", "天王", "海王", "冥王"],
            //         '四軸': ["上升", "下降", "天頂", "天底"],
            //         '命運與潛意識': ["北交", "南交", "宿命", "福點", "莉莉絲"],
            //         '小行星': ["凱龍", "穀神", "智神", "婚神", "灶神", "愛神", "靈神", "人龍"]
            //     };
            //     const container = document.getElementById('optionalPlanetsContainer');
            //     container.innerHTML = ''; // 清空

            //     // 修改1動態生成所有內容
            //     for (const groupName in optionalPlanetsConfig) {
            //         // 建立一個包含標題和按鈕的 header div
            //         const headerDiv = document.createElement('div');
            //         headerDiv.className = 'planet-group-header col-span-full mt-2'; // 使用新的 CSS class

            //         // 建立分類標題
            //         const groupTitle = document.createElement('span');
            //         groupTitle.className = 'font-semibold text-lg text-fuchsia-900';
            //         groupTitle.textContent = groupName;

            //         // 建立分類切換按鈕
            //         const groupToggleButton = document.createElement('button');
            //         groupToggleButton.className = 'planet-toggle-btn group-toggle-btn'; // 通用按鈕樣式 + 分類按鈕的專屬 class
            //         groupToggleButton.textContent = '此類取消';
            //         groupToggleButton.dataset.state = 'all-checked';
            //         groupToggleButton.dataset.groupKey = groupName; // 用 data-* 屬性記住它屬於哪個分類

            //         headerDiv.appendChild(groupTitle);
            //         headerDiv.appendChild(groupToggleButton);
            //         container.appendChild(headerDiv);

            //         // 生成該分類下的所有 checkbox
            //         optionalPlanetsConfig[groupName].forEach(planet => {
            //             const wrapper = document.createElement('div');
            //             wrapper.className = 'flex items-center';
            //             wrapper.innerHTML = `
            //     <input id="chk-${planet}" type="checkbox" value="${planet}" class="optional-planet-checkbox h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" data-group="${groupName}" checked>
            //     <label for="chk-${planet}" class="ml-2 block text-lg text-gray-900">${planet}</label>
            // `;
            //             container.appendChild(wrapper);
            //         });
            //     }

            //     // 修改2使用「事件代理」來統一處理所有按鈕的點擊事件，更高效
            //     const selectionDiv = document.getElementById('planetSelection');
            //     selectionDiv.addEventListener('click', (event) => {
            //         const target = event.target;

            //         // --- 判斷點擊的是「總開關」按鈕 ---
            //         if (target.id === 'toggleAllPlanetsBtn') {
            //             const checkboxes = document.querySelectorAll('.optional-planet-checkbox');
            //             const isChecked = target.dataset.state === 'all-checked';
            //             checkboxes.forEach(cb => { cb.checked = !isChecked; });
            //             target.textContent = isChecked ? '全部選取' : '全部取消';
            //             target.dataset.state = isChecked ? 'all-unchecked' : 'all-checked';

            //             // 同步更新所有分類按鈕的狀態和文字
            //             document.querySelectorAll('.group-toggle-btn').forEach(btn => {
            //                 btn.textContent = isChecked ? '此類別選取' : '此類取消';
            //                 btn.dataset.state = isChecked ? 'all-unchecked' : 'all-checked';
            //             });
            //         }

            //         // --- 判斷點擊的是「分類」按鈕 ---
            //         if (target.classList.contains('group-toggle-btn')) {
            //             const groupKey = target.dataset.groupKey;
            //             const checkboxesInGroup = document.querySelectorAll(`.optional-planet-checkbox[data-group="${groupKey}"]`);
            //             const isChecked = target.dataset.state === 'all-checked';
            //             checkboxesInGroup.forEach(cb => { cb.checked = !isChecked; });
            //             target.textContent = isChecked ? '此類別選取' : '此類取消';
            //             target.dataset.state = isChecked ? 'all-unchecked' : 'all-checked';
            //         }
            //     });

            //     // 最後，確保最上面的總按鈕也套用新樣式
            //     document.getElementById('toggleAllPlanetsBtn').className = 'planet-toggle-btn all-toggle-btn';
            // }

            // 設定輸入時自動清除錯誤提示
            function setupInputErrorClearing() {
                document.querySelectorAll('.input-field, .select-field').forEach(input => {
                    const clearError = (event) => {
                        const errorElementId = `${event.target.id}-error`;
                        const errorElement = document.getElementById(errorElementId);
                        if (errorElement) {
                            errorElement.textContent = '';
                            errorElement.style.display = 'none';
                            event.target.style.setProperty('--input-border-color', '#cbd5e0');
                        }
                        // Special handling for timezone pairs
                        const container = event.target.closest('.timezone-input-group-container');
                        if (container) {
                            const relatedErrorId = container.querySelector('.timezone-select').id + '-error';
                            const relatedErrorElement = document.getElementById(relatedErrorId);
                            if (relatedErrorElement) {
                                relatedErrorElement.textContent = '';
                                relatedErrorElement.style.display = 'none';
                            }
                            container.querySelectorAll('.input-field, .select-field').forEach(el => el.style.setProperty('--input-border-color', '#cbd5e0'));
                        }
                    };
                    input.addEventListener('input', clearError);
                    input.addEventListener('change', clearError);
                });
            }

            // 設定時區下拉選單與手動輸入的連動
            function setupCustomTimezoneListeners() {
                document.querySelectorAll('.timezone-input-group-container').forEach(container => {
                    const selectEl = container.querySelector('.select-field');
                    const customInputEl = container.querySelector('.input-field');
                    if (selectEl && customInputEl) {
                        selectEl.addEventListener('change', () => {
                            if (selectEl.value !== '') customInputEl.value = '';
                        });
                        customInputEl.addEventListener('input', () => {
                            if (customInputEl.value.trim() !== '') selectEl.value = '';
                        });
                    }
                });
            }

            // =============================================================
            // 核心功能函式
            // =============================================================

            // 更新主頁籤介面
            function updateMainTabVisibility(activeTabId) {
                const body = document.body;
                body.classList.remove('bg-single', 'bg-synastry');
                body.classList.add(activeTabId === 'singleChartTab' ? 'bg-single' : 'bg-synastry');

                document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
                document.getElementById(activeTabId).classList.add('active');

                document.querySelectorAll('.chart-section').forEach(sec => sec.classList.add('hidden'));
                const contentId = document.getElementById(activeTabId).dataset.tabContent;
                document.getElementById(contentId).classList.remove('hidden');
            }

            // 更新雙人盤子選項介面
            function updateSubChartVisibility(selectedType) {
                document.querySelectorAll('.chart-card-sub').forEach(card => card.classList.remove('active'));
                document.querySelector(`.chart-card-sub[data-chart-type="${selectedType}"]`).classList.add('active');
                document.getElementById('selectedSubChartType').value = selectedType;

                document.getElementById('comparisonChartInputs').classList.add('hidden');
                document.getElementById('transitChartInputs').classList.add('hidden');

                if (selectedType === 'comparison' || selectedType === 'composite') {
                    document.getElementById('comparisonChartInputs').classList.remove('hidden');
                } else if (selectedType === 'transit') {
                    document.getElementById('transitChartInputs').classList.remove('hidden');
                }
            }

            // 填充時區下拉選單
            function populateTimezoneSelects() {
                const getOffsetString = (tz) => {
                    try {
                        const offset = new Intl.DateTimeFormat('en-US', { timeZone: tz, timeZoneName: 'shortOffset' }).formatToParts().find(p => p.type === 'timeZoneName').value;
                        let alias = tz.split('/').pop().replace(/_/g, ' ');
                        if (tz === "Asia/Taipei") alias = "台北";
                        if (tz === "Asia/Shanghai") alias = "上海";
                        if (tz === "Asia/Tokyo") alias = "東京";
                        return `${offset} ${alias}`;
                    } catch (e) {
                        return tz;
                    }
                };

                const sortedTimezones = commonTimezones.map(tz => ({ value: tz, text: getOffsetString(tz) }))
                    .sort((a, b) => a.text.localeCompare(b.text, 'en'));

                document.querySelectorAll('.timezone-select').forEach(selectElement => {
                    selectElement.innerHTML = '';
                    sortedTimezones.forEach(opt => {
                        const option = new Option(opt.text, opt.value);
                        selectElement.add(option);
                    });
                    selectElement.value = "Asia/Taipei"; // Default
                });
            }

            // 輸入驗證
            function validateInputs(prefix) {
                let isValid = true;
                const fields = {
                    'year': { min: 1900, max: 2100, label: '年份' }, 'month': { min: 1, max: 12, label: '月份' },
                    'day': { min: 1, max: 31, label: '日期' }, 'hour': { min: 0, max: 23, label: '時' },
                    'minute': { min: 0, max: 59, label: '分' }, 'latitude': { min: -90, max: 90, label: '緯度' },
                    'longitude': { min: -180, max: 180, label: '經度' }
                };

                for (const field in fields) {
                    const inputId = `${prefix}${field}`;
                    const inputElement = document.getElementById(inputId);
                    const value = inputElement.value;
                    const parsedValue = parseFloat(value);
                    const { min, max, label } = fields[field];

                    if (value.trim() === '' || isNaN(parsedValue) || parsedValue < min || parsedValue > max) {
                        showInputError(inputId, `請輸入有效的${label} (${min}-${max})。`);
                        isValid = false;
                    }
                }

                const timezoneSelect = document.getElementById(`${prefix}timezone`);
                const customTimezoneInput = document.getElementById(`${prefix}customTimezone`);
                if (!timezoneSelect.value && !customTimezoneInput.value.trim()) {
                    showInputError(timezoneSelect.id, '請選擇或手動輸入時區。');
                    customTimezoneInput.style.setProperty('--input-border-color', '#ef4444');
                    isValid = false;
                }
                return isValid;
            }

            

            // toggle 小行星/虛點選項內容
            document.addEventListener('DOMContentLoaded', () => {
    // 取得新的元素
    const toggleHeader = document.getElementById('toggleHeader');
    const toggleIcon = document.getElementById('toggleIcon');
    const toggleAllPlanetsBtn = document.getElementById('toggleAllPlanetsBtn');
    const optionalPlanetsContainer = document.getElementById('optionalPlanetsContainer');

    // 為標題新增點擊事件
    toggleHeader.addEventListener('click', () => {
        const isHidden = optionalPlanetsContainer.classList.contains('hidden');

        if (isHidden) {
            // 展開時
            optionalPlanetsContainer.classList.remove('hidden');
            toggleAllPlanetsBtn.classList.remove('hidden');
            toggleIcon.classList.remove('rotate-0');
            toggleIcon.classList.add('rotate-90');
        } else {
            // 收合時
            optionalPlanetsContainer.classList.add('hidden');
            toggleAllPlanetsBtn.classList.add('hidden');
            toggleIcon.classList.remove('rotate-90');
            toggleIcon.classList.add('rotate-0');
        }
    });
});


            // 主要計算函式
            async function calculateChart() {
                console.log('Calculate button clicked.');
                clearAllInputErrors();
                const resultOutput = document.getElementById('resultOutput');
                const loadingSpinner = document.getElementById('loadingSpinner');
                const textOutputArea = document.getElementById('tableTextDisplayArea');
                const outputToggleButtons = document.getElementById('outputToggleButtons');


                resultOutput.innerHTML = '';
                resultOutput.classList.remove('error-message');

                // --> START OF MODIFICATION IN calculateChart FUNCTION <--
                // 初始化隱藏顯示區域和切換按鈕，清空之前結果
                if (textOutputArea) textOutputArea.innerHTML = ''; // 清空之前結果
                if (outputToggleButtons) outputToggleButtons.style.display = 'none';
                // --> END OF MODIFICATION IN calculateChart FUNCTION <--

                const getInputValue = (id) => document.getElementById(id)?.value || '';
                let payload = {};
                let apiUrl = '';
                let chart1Name = '';
                let chart2Name = '';
                let isValid = true;

                const optionalPlanets = Array.from(document.querySelectorAll('.optional-planet-checkbox:checked')).map(cb => cb.value);

                const activeMainTabId = document.querySelector('.tab-button.active').id;

                if (activeMainTabId === 'singleChartTab') {
                    chart1Name = getInputValue('single_name') || "我的星盤";
                    isValid = validateInputs('single_');
                    if (isValid) {
                        payload = {
                            year: parseInt(getInputValue('single_year')), month: parseInt(getInputValue('single_month')), day: parseInt(getInputValue('single_day')),
                            hour: parseInt(getInputValue('single_hour')), minute: parseInt(getInputValue('single_minute')),
                            latitude: parseFloat(getInputValue('single_latitude')), longitude: parseFloat(getInputValue('single_longitude')),
                            timezone: getInputValue('single_customTimezone') || getInputValue('single_timezone'),
                            optional_planets: optionalPlanets // 將正確收集的列表放入 payload
                        };
                        apiUrl = `${BASE_API_URL}/calculate_single_chart`;
                    }
                } else { // synastryChartSection
                    const subChartType = document.getElementById('selectedSubChartType').value;
                    if (subChartType === 'transit') {
                        chart1Name = getInputValue('natal_name') || "本命";
                        chart2Name = getInputValue('transit_name') || "行運";
                        isValid = validateInputs('natal_') && validateInputs('transit_');
                        if (isValid) {
                            payload = {
                                natal_year: parseInt(getInputValue('natal_year')), natal_month: parseInt(getInputValue('natal_month')), natal_day: parseInt(getInputValue('natal_day')),
                                natal_hour: parseInt(getInputValue('natal_hour')), natal_minute: parseInt(getInputValue('natal_minute')),
                                natal_latitude: parseFloat(getInputValue('natal_latitude')), natal_longitude: parseFloat(getInputValue('natal_longitude')),
                                natal_timezone: getInputValue('natal_customTimezone') || getInputValue('natal_timezone'),
                                transit_year: parseInt(getInputValue('transit_year')), transit_month: parseInt(getInputValue('transit_month')), transit_day: parseInt(getInputValue('transit_day')),
                                transit_hour: parseInt(getInputValue('transit_hour')), transit_minute: parseInt(getInputValue('transit_minute')),
                                transit_latitude: parseFloat(getInputValue('transit_latitude')), transit_longitude: parseFloat(getInputValue('transit_longitude')),
                                transit_timezone: getInputValue('transit_customTimezone') || getInputValue('transit_timezone'),
                                optional_planets: optionalPlanets // 將正確收集的列表放入 payload
                            };
                            apiUrl = `${BASE_API_URL}/calculate_transit_chart`;
                        }
                    } else { // comparison or composite
                        chart1Name = getInputValue('comp1_name') || "您";
                        chart2Name = getInputValue('comp2_name') || "對方";
                        isValid = validateInputs('comp1_') && validateInputs('comp2_');
                        if (isValid) {
                            payload = {
                                chart1_year: parseInt(getInputValue('comp1_year')), chart1_month: parseInt(getInputValue('comp1_month')), chart1_day: parseInt(getInputValue('comp1_day')),
                                chart1_hour: parseInt(getInputValue('comp1_hour')), chart1_minute: parseInt(getInputValue('comp1_minute')),
                                chart1_latitude: parseFloat(getInputValue('comp1_latitude')), chart1_longitude: parseFloat(getInputValue('comp1_longitude')),
                                chart1_timezone: getInputValue('comp1_customTimezone') || getInputValue('comp1_timezone'),
                                chart2_year: parseInt(getInputValue('comp2_year')), chart2_month: parseInt(getInputValue('comp2_month')), chart2_day: parseInt(getInputValue('comp2_day')),
                                chart2_hour: parseInt(getInputValue('comp2_hour')), chart2_minute: parseInt(getInputValue('comp2_minute')),
                                chart2_latitude: parseFloat(getInputValue('comp2_latitude')), chart2_longitude: parseFloat(getInputValue('comp2_longitude')),
                                chart2_timezone: getInputValue('comp2_customTimezone') || getInputValue('comp2_timezone'),
                                optional_planets: optionalPlanets // 將正確收集的列表放入 payload
                            };
                            if (subChartType === 'composite') {
                                payload.composite_method = 'reference_plane'; // Hardcoded as per UI
                                apiUrl = `${BASE_API_URL}/calculate_composite_chart`;
                            } else {
                                apiUrl = `${BASE_API_URL}/calculate_comparison_chart`;
                            }
                        }
                    }
                }

                if (!isValid) {
                    resultOutput.textContent = "❌ 請更正上方標示的錯誤後再試。";
                    resultOutput.classList.add('error-message');
                    return;
                }

                loadingSpinner.style.display = 'inline-block';

                try {
                    // 發送 Axios POST 請求
                    const response = await axios.post(apiUrl, payload, {
                        headers: {
                            'X-API-Key': YOUR_API_KEY // 確保你的 API Key 被正確傳送
                        }
                    });

                    // 成功響應：將數據傳遞給 displayChartData 函數進行統一處理
                    displayChartData(response.data, chart1Name, chart2Name);

                    // 呼叫 setupCopyListeners 函式
                    setupCopyListeners(); 


                } catch (error) {
                    // 錯誤處理邏輯 (你現有的)
                    resultOutput.classList.add('error-message');
                    if (error.response) {
                        const errorData = error.response.data;
                        if (error.response.status === 400 && errorData?.error_type === 'invalid_timezone') {
                            resultOutput.textContent = '❌ 時區輸入錯誤，請修正上方標示的欄位。';
                            const prefix = (errorData.error_source === 'chart1') ? 'comp1_' : 'comp2_';
                            showInputError(`${prefix}timezone`, errorData.error);
                        } else if (error.response.status === 401 || error.response.status === 403) { // 新增 API Key 相關錯誤處理
                            resultOutput.textContent = '❌ 認證失敗：API Key 無效或缺失。';
                        }
                        else {
                            resultOutput.textContent = `❌ 伺服器錯誤 ${error.response.status}: ${errorData?.error || '未知錯誤'}`;
                        }
                    } else if (error.request) {
                        resultOutput.textContent = '❌ 網路錯誤：無法連接到伺服器。';
                    } else {
                        resultOutput.textContent = `❌ 請求錯誤：${error.message}`;
                    }
                    // --> START OF MODIFICATION IN calculateChart FUNCTION (Error part) <--
                    // 錯誤時隱藏結果區域和切換按鈕
                    if (outputToggleButtons) outputToggleButtons.style.display = 'none';
                    if (textOutputArea) textOutputArea.style.display = 'none';
                    // --> END OF MODIFICATION IN calculateChart FUNCTION (Error part) <--

                } finally {
                    loadingSpinner.style.display = 'none';
                }
            }


            // 生成兩種交互相位
            function generateFullInterAspectsHTML(aspects, name1, name2) {
    // 檢查數據是否存在
    if (!aspects || aspects.length === 0) {
        // 如果沒有相位，返回一個提示訊息
        return `<div class="result-section-item">
                    <div class="result-section-header">
                        <h2>交互相位</h2>
                        <div class="section-content">
                            <p>雙方之間沒有偵測到交互相位。</p>
                        </div>
                    </div>
                </div>`;
    }

    // 第一步：生成「${name1}的星體與${name2}的星體」的交互相位內容
    const sectionsDataAtoB = generateInterAspectsSectionData(aspects, name1, name2);
    const htmlAtoB = `
        <div class="result-section-item">
            ${createResultSection(`交互相位：${name1}的星體與${name2}的星體`, sectionsDataAtoB.table, sectionsDataAtoB.narrative, false, 'interaction-header-style')}
        </div>`;

    // 第二步：創建反轉的數據
    const reversedAspects = aspects.map(a => ({
        ...a, // 複製所有屬性
        p1_name: a.p2_name, // 星體1變星體2
        p2_name: a.p1_name, // 星體2變星體1
        // 注意：這裡的 p1_pos 和 p2_pos 如果需要，也應對調
        // 但因為 generateInterAspectsSectionData 函數沒有用到它們，所以可以省略
    }));

    // 第三步：生成「${name2}的星體與${name1}的星體」的交互相位內容
    const sectionsDataBtoA = generateInterAspectsSectionData(reversedAspects, name2, name1);
    const htmlBtoA = `
        <div class="result-section-item">
            ${createResultSection(`交互相位：${name2}的星體與${name1}的星體`, sectionsDataBtoA.table, sectionsDataBtoA.narrative, false, 'interaction-header-style')}
        </div>`;

    // 第四步：將兩個 HTML 區塊拼接起來
    return htmlAtoB + htmlBtoA;
}

            // =============================================================
            // 結果顯示與 HTML 生成
            // =============================================================

            // 主顯示函式
            // 請用此版本完整取代 astro__.html 裡面舊的 displayChartData 函式
            function displayChartData(data, name1, name2) {
                const container = document.getElementById('resultOutput');
                if (!container) {
                    console.error("找不到 ID 為 'resultOutput' 的容器。");
                    return;
                }

                container.innerHTML = '';

                let reportHtmlContent = '';
                let rawJsonString = '';

                try {
                    rawJsonString = JSON.stringify(data, null, 2);
                } catch (e) {
                    console.error("Error converting data to JSON string:", e);
                    rawJsonString = "Error: Could not convert data to JSON string.";
                }

                switch (data.chart_type) {
                    case 'single':
                        // 步驟 1: 先呼叫 generateSingleChartSectionData 來準備好所有章節的表格和敘述文本
                        const singleChartSectionsData = generateSingleChartSectionData(data, `${name1}的星盤文字資訊`);

                        // 步驟 2: 然後將準備好的 sectionsData 傳遞給 buildSingleChartHTML 進行 HTML 結構的組裝
                        reportHtmlContent = buildSingleChartHTML(singleChartSectionsData, `${name1}的星盤文字資訊`);
                        break;

                    case 'comparison':
                        // --- 新增的變數來明確主盤和訪客的姓名 ---
                        // name1 (comp1_name) 是主盤，name2 (comp2_name) 是訪客
                        const finalHostName = name1;
                        const finalGuestName = name2;

                        // 1. 生成並構建第一個本命盤的 HTML
                        const natal1SectionsData = generateSingleChartSectionData(data.chart1_data, `${finalHostName}的本命盤`);
                        const natal1Html = buildSingleChartHTML(natal1SectionsData, `${finalHostName}的本命盤`);

                        // 2. 生成並構建第二個本命盤的 HTML
                        const natal2SectionsData = generateSingleChartSectionData(data.chart2_data, `${finalGuestName}的本命盤`);
                        const natal2Html = buildSingleChartHTML(natal2SectionsData, `${finalGuestName}的本命盤`);

                        // 3. 生成並構建交互相位和疊盤的 HTML
                        let interactionHtmlComparison = `<div class="sub-sections-container">`;

                        // --- 3.1 訪客星體落入主盤宮位 (Overlay: `name2` 的星體落入 `name1` 的宮位) ---
                        // API 數據是 `data.chart2_planets_in_chart1_houses`
                        const titleGuestIntoHost = `${finalGuestName}星體落入${finalHostName}宮位`;
                        const overlayGuestIntoHostSectionsData = generateOverlaySectionData(
                            data.chart2_planets_in_chart1_houses, // 👈 數據：訪客(chart2)行星在主盤(chart1)宮位
                            finalGuestName,                       // 👈 Guest Name (訪客)
                            finalHostName,                        // 👈 Host Name (主盤)
                            titleGuestIntoHost                    // 👈 完整標題
                        );
                        interactionHtmlComparison += buildOverlayHTML(
                            overlayGuestIntoHostSectionsData,
                            finalGuestName,                       // 👈 Guest Name
                            finalHostName,                        // 👈 Host Name
                            titleGuestIntoHost                    // 👈 完整標題
                        );

                        // --- 3.2 主盤星體落入訪客宮位 (Overlay: `name1` 的星體落入 `name2` 的宮位) ---
                        // API 數據是 `data.chart1_planets_in_chart2_houses`
                        const titleHostIntoGuest = `${finalHostName}星體落入${finalGuestName}宮位`;
                        const overlayHostIntoGuestSectionsData = generateOverlaySectionData(
                            data.chart1_planets_in_chart2_houses, // 👈 數據：主盤(chart1)行星在訪客(chart2)宮位
                            finalHostName,                        // 👈 Guest Name (這裡的主盤相對這個報告是「被看」的客人)
                            finalGuestName,                       // 👈 Host Name (這裡的訪客相對這個報告是「被落入」的盤主)
                            titleHostIntoGuest                    // 👈 完整標題
                        );
                        interactionHtmlComparison += buildOverlayHTML(
                            overlayHostIntoGuestSectionsData,
                            finalHostName,
                            finalGuestName,
                            titleHostIntoGuest
                        );

                        // // 3.3 交互相位
                        // // 先生成兩種格式的內容數據
                        // const interAspectsSectionsDataComparison = generateInterAspectsSectionData(data.inter_aspects, name1, name2);
                        // // 再將數據傳給 HTML 組裝函數 (注意：buildInterAspectsHTML 的簽名已調整)
                        // interactionHtmlComparison += buildInterAspectsHTML(interAspectsSectionsDataComparison, name1, name2);

                        // interactionHtmlComparison += `</div>`; // 關閉 sub-sections-container


                        // 3.3 交互相位 (改為雙向生成)

// 步驟一：生成「${name1}的星體與${name2}的星體」的交互相位內容
const sectionsDataAtoB = generateInterAspectsSectionData(data.inter_aspects, name1, name2);

// 步驟二：創建反轉的數據，用來生成另一方向的內容
const reversedAspects = data.inter_aspects.map(a => ({
    ...a, // 複製所有屬性
    p1_name: a.p2_name, // 星體1變星體2
    p2_name: a.p1_name, // 星體2變星體1
}));

// 步驟三：生成「${name2}的星體與${name1}的星體」的交互相位內容
const sectionsDataBtoA = generateInterAspectsSectionData(reversedAspects, name2, name1);

// 步驟四：將兩個方向的數據傳入一個新的 HTML 組裝函數，一次生成兩個區塊
// 這裡假設你已經根據我之前的教學，將 buildInterAspectsHTML 函數改寫成可以處理兩個方向的數據。
interactionHtmlComparison += buildInterAspectsHTML(sectionsDataAtoB, sectionsDataBtoA, name1, name2);

                        // 4. 組裝最終的報告 HTML
                        reportHtmlContent = createReportWrapper(`${name1}與${name2}的比較盤報告`, natal1Html + natal2Html + interactionHtmlComparison);
                        break;

                    case 'composite':
                        // Step 1: Generate the section data for the Composite Chart
                        const compositeSectionsData = generateSingleChartSectionData(data.composite_chart_data, `${name1}與${name2}的組合中點盤`);
                        // Step 2: Build the HTML for the Composite Chart using the generated data
                        const compositeHtml = buildSingleChartHTML(compositeSectionsData, `${name1}與${name2}的組合中點盤`, 'composite-chart-header-style');

                        // Step 3: Generate the section data for Natal Chart 1
                        const ref1SectionsData = generateSingleChartSectionData(data.natal_chart1_data, `${name1}的本命盤`);
                        // Step 4: Build the HTML for Natal Chart 1 using the generated data
                        const ref1Html = buildSingleChartHTML(ref1SectionsData, `${name1}的本命盤`);

                        // Step 5: Generate the section data for Natal Chart 2
                        const ref2SectionsData = generateSingleChartSectionData(data.natal_chart2_data, `${name2}的本命盤`);
                        // Step 6: Build the HTML for Natal Chart 2 using the generated data
                        const ref2Html = buildSingleChartHTML(ref2SectionsData, `${name2}的本命盤`);

                        // Step 7: Wrap all the generated chart HTML into the final report structure
                        reportHtmlContent = createReportWrapper('組合中點盤報告', compositeHtml + ref1Html + ref2Html);
                        break;

                    case 'transit':
                        // Define transitDateTime early as it's used in the title
                        const transitDateTime = data.transit_chart_data.timestamps.local_time;

                        // --- 單個星盤的生成與構建 ---
                        // Step 1: Generate section data for the Natal Chart
                        const transitNatalSectionsData = generateSingleChartSectionData(data.natal_chart_data, `${name1}的本命盤`);
                        // Step 2: Build HTML for the Natal Chart
                        const transitNatalHtml = buildSingleChartHTML(transitNatalSectionsData, `${name1}的本命盤`);

                        // Step 3: Generate section data for the Transit Chart
                        const transitChartSectionsData = generateSingleChartSectionData(data.transit_chart_data, `${transitDateTime} 行運天象盤`);
                        // Step 4: Build HTML for the Transit Chart
                        const transitChartHtml = buildSingleChartHTML(transitChartSectionsData, `${transitDateTime} 行運天象盤`);

                        // --- 交互部分的生成與構建 ---
                        let transitInteractionHtml = `<div class="sub-sections-container">`; // 使用不同的變數名

                        // 行運星體落入本命宮位：guestName 是 "行運"，hostName 是 name1 (本命盤主人)
                        // 先生成兩種格式的內容數據
                        // 定義一個明確的標題變數，方便統一管理
                        const transitOverlayTitle = `行運星體落入${name1}宮位`; // 這裡可以根據需要調整標題的顯示方式
                        const transitOverlaySectionsData = generateOverlaySectionData(
                            data.transit_planets_in_natal_houses,
                            "行運", // 訪客姓名 (Guest Name)
                            name1,  // 主盤姓名 (Host Name)
                            transitOverlayTitle // 完整的標題字串
                        );

                        // 🚨 這裡就是你需要修改的地方！確保傳入四個參數。
                        transitInteractionHtml += buildOverlayHTML(
                            transitOverlaySectionsData,
                            "行運",             // 👈 訪客姓名 (Guest Name)
                            name1,              // 👈 主盤姓名 (Host Name)
                            transitOverlayTitle // 👈 完整的標題字串
                        );

                        // 行運與本命的交互相位
                        // 先生成兩種格式的內容數據
                        const transitInterAspectsSectionsData = generateInterAspectsSectionData(data.inter_aspects, name1, "行運", true);
                        // 再將數據傳給 HTML 組裝函數 (注意：buildInterAspectsHTML 的簽名已調整)
                        transitInteractionHtml += buildInterAspectsHTML(transitInterAspectsSectionsData, name1, "行運", true);

                        transitInteractionHtml += `</div>`; // 關閉 sub-sections-container

                        // Step 5: Wrap all the generated chart HTML and interaction HTML into the final report structure
                        reportHtmlContent = createReportWrapper(`${name1}的行運盤報告`, transitInteractionHtml + transitNatalHtml + transitChartHtml);
                        break;

                    default:
                        reportHtmlContent = `<div class="error-message">錯誤: 未知的星盤類型 '${data.chart_type}'</div>`;
                }

                // 完整的組合 HTML 內容，包含你提供的所有結構
                const combinedHtml = `
        <div class="main-report-content report-full-content">
            ${reportHtmlContent}
        </div>`;

                container.innerHTML = combinedHtml; // 將所有內容一次性注入

                // 在 DOM 更新後，呼叫事件綁定函數
                setupCopyListeners();

                // 【核心修正 1】: 重新套用使用者當前選擇的顯示模式 (表格或敘述)
                updateDisplayMode(currentDisplayMode);
            }

            // 新增的輔助函數：生成單一星盤各部分的數據（表格和敘述兩種格式）
            // 它會接收原始的 chartInfo 和圖表標題 (title)，因為基礎數據的判斷依賴 title
            function generateSingleChartSectionData(chartInfo, chartTitle) {
                // 錯誤處理：如果 chartInfo 不存在，返回空物件或帶有錯誤信息的物件
                if (!chartInfo) {
                    return {
                        summary: { table: "資料缺失", narrative: "星盤資料缺失，無法提供詳細資訊。" },
                        cusp: { table: "宮頭數據缺失", narrative: "宮頭數據缺失，無法提供完整敘述。" },
                        planet: { table: "星體數據缺失", narrative: "星體數據缺失，無法提供完整敘述。" },
                        aspect: { table: "沒有相位", narrative: "本命盤中沒有偵測到主要相位。" }
                    };
                }

                const { timestamps, birth_info, house_cusps, planet_positions, aspects } = chartInfo;

                const sectionsData = {}; // 儲存所有部分的表格和敘述文本

                // --- 1. 基礎數據 (Summary Content) ---
                sectionsData.summary = {};
                if (chartTitle.includes("組合中點盤")) {
                    sectionsData.summary.table = [
                        "==== 組合中點盤盤資訊 ====",
                        "組合中點盤為兩張本命盤的數學中點取得的星盤",
                        "====================\n"
                    ].join('\n');
                    sectionsData.summary.narrative = "星盤基礎資訊\n組合中點盤是透過數學方式計算兩張本命盤中點所形成的特殊星盤，用於探索兩人關係的獨立生命本質。\n";
                } else {
                    sectionsData.summary.table = (timestamps && birth_info) ? [
                        "\n==== 星盤基礎數據 ====\n",
                        `本地時間: ${timestamps.local_time}`,
                        `UTC 時間: ${timestamps.utc_time}`,
                        `緯度: ${birth_info.latitude}, 經度: ${birth_info.longitude}`,
                        "\n====================\n"
                    ].join('\n') : "基礎數據缺失";

                    sectionsData.summary.narrative = (timestamps && birth_info) ?
                        `\n==== 星盤基礎數據 ====\n本地時間：${timestamps.local_time}\nUTC時間：${timestamps.utc_time}\n出生地座標：緯度 ${birth_info.latitude}, 經度 ${birth_info.longitude}\n====================\n` :
                        "基礎數據缺失，無法提供完整敘述。\n";
                }

                // --- 2. 宮頭 (Cusp Content) ---
                sectionsData.cusp = {};
                if (house_cusps?.length > 0) {
                    sectionsData.cusp.table = [ // 表格內容不變
                        "==== 宮頭 ====",
                        "宮頭 | 星座度數(度分)",
                        "--------------------", // 表格分隔線
                        ...house_cusps.map(c => `${c.house_number}宮 | ${c.zodiac_position_formatted}`),
                        "============\n"
                    ].join('\n');

                    // 【核心修正 2】: 在分隔線後方加上換行符 `\n`
                    sectionsData.cusp.narrative = "==== 宮頭 ====\n";
                    house_cusps.forEach(c => {
                        // 敘述版沒有表格分隔線
                        sectionsData.cusp.narrative += `${c.house_number} 宮頭: ${c.zodiac_position_formatted}\n`;
                    });
                    sectionsData.cusp.narrative += "====================\n";// 段落間距
                } else {
                    sectionsData.cusp.table = "宮頭數據缺失";
                    sectionsData.cusp.narrative = "宮頭數據缺失，無法提供完整敘述。\n";
                }

                // --- 3. 星體位置 (Planet Content) ---
                sectionsData.planet = {};
                if (planet_positions) {
                    sectionsData.planet.table = [ // 表格內容不變
                        "==== 星體位置 ====",
                        "星體 | 順逆 | 星座度數(度分) | 宮位(度分)",
                        "-----------------------------", // 表格分隔線
                        ...DISPLAY_ORDER_NAMES // 假設 DISPLAY_ORDER_NAMES 是已定義的全局常量
                            .filter(name => planet_positions[name])
                            .map(name => {
                                const p = planet_positions[name];
                                // 假設 HOUSE_DEFINING_POINTS 是已定義的全局常量
                                // 假設 formatDegreesMinutesSeconds 是已定義的全局函數
                                const houseInfo = !HOUSE_DEFINING_POINTS.includes(name) && p.house != null
                                    ? `${p.house}宮(${formatDegreesMinutesSeconds(p.hdeg)})` : '-';
                                return `${name} | ${p.is_retrograde ? '逆行' : ''} | ${p.zodiac_position_formatted} | ${houseInfo}`;
                            }),
                        "================\n"
                    ].join('\n');

                    // 【核心修正 2】: 在分隔線後方加上換行符 `\n`
                    sectionsData.planet.narrative = "==== 星體位置 ====\n";
                    DISPLAY_ORDER_NAMES
                        .filter(name => planet_positions[name])
                        .forEach(name => {
                            const p = planet_positions[name];
                            const houseText = !HOUSE_DEFINING_POINTS.includes(name) && p.house != null
                                ? `${p.house}宮(${formatDegreesMinutesSeconds(p.hdeg)})` : '';
                            const retrogradeText = p.is_retrograde ? '逆行' : '';
                            // 敘述版中，如果沒有宮位資訊則不顯示
                            const positionAndHouse = p.zodiac_position_formatted + (houseText ? houseText : '');
                            sectionsData.planet.narrative += `${name}${retrogradeText} ${positionAndHouse}\n`;
                        });
                    sectionsData.planet.narrative += "====================\n";// 段落間距
                } else {
                    sectionsData.planet.table = "星體數據缺失";
                    sectionsData.planet.narrative = "星體數據缺失，無法提供完整敘述。\n";
                }

                // --- 4. 主要相位 (Aspect Content) ---
                sectionsData.aspect = {};
                if (aspects?.length > 0) {
                    // 【核心修正】確保相位智慧排序且不重複
                    // 步驟 1: 正規化相位，確保 p1_name 的行星順序總是在 p2_name 之前
                    const normalizedAspects = aspects.map(a => {
                        const p1Index = DISPLAY_ORDER_NAMES.indexOf(a.p1_name);
                        const p2Index = DISPLAY_ORDER_NAMES.indexOf(a.p2_name);
                        // 如果 p1 的順序在 p2 之後，則交換它們，以建立一個唯一的識別
                        if (p1Index > p2Index) {
                            return { ...a, p1_name: a.p2_name, p2_name: a.p1_name };
                        }
                        return a;
                    });

                    // 步驟 2: 過濾掉重複的相位
                    // 我們只保留陣列中第一次出現的 `p1-p2-aspect` 組合
                    const uniqueAspects = normalizedAspects.filter((aspect, index, self) =>
                        index === self.findIndex(t =>
                            t.p1_name === aspect.p1_name &&
                            t.p2_name === aspect.p2_name &&
                            t.aspect_name === aspect.aspect_name
                        )
                    );

                    // 步驟 3: 對唯一的相位列表進行最終排序
                    const sortedAspects = uniqueAspects.sort((a, b) => {
                        const p1aIndex = DISPLAY_ORDER_NAMES.indexOf(a.p1_name);
                        const p1bIndex = DISPLAY_ORDER_NAMES.indexOf(b.p1_name);
                        if (p1aIndex !== p1bIndex) {
                            return p1aIndex - p1bIndex;
                        }
                        const p2aIndex = DISPLAY_ORDER_NAMES.indexOf(a.p2_name);
                        const p2bIndex = DISPLAY_ORDER_NAMES.indexOf(b.p2_name);
                        return p2aIndex - p2bIndex;
                    });

                    // 使用處理過的 `sortedAspects` 來生成表格和敘述
                    sectionsData.aspect.table = [
                        "==== 主要相位 ====",
                        "星體1 | 相位 | 星體2 | 動態 | 容許度",
                        "----------------------", // 表格分隔線
                        ...sortedAspects.map(a => `${a.p1_name} | ${a.aspect_name} | ${a.p2_name} | ${a.aspect_type || '-'} | ${formatDegreesMinutesSeconds(a.orb)}`),
                        "================\n"
                    ].join('\n');

                    // 【核心修正 2】: 在分隔線後方加上換行符 `\n`
                    sectionsData.aspect.narrative = "==== 主要相位 ====\n";
                    aspects.sort((a, b) => DISPLAY_ORDER_NAMES.indexOf(a.p1_name) - DISPLAY_ORDER_NAMES.indexOf(b.p1_name) || DISPLAY_ORDER_NAMES.indexOf(a.p2_name) - DISPLAY_ORDER_NAMES.indexOf(b.p2_name)).forEach(a => {
                        const p1 = planet_positions[a.p1_name];
                        const p1HouseInfo = p1 && !HOUSE_DEFINING_POINTS.includes(a.p1_name) && p1.house != null
                            ? `${p1.house}宮(${formatDegreesMinutesSeconds(p1.hdeg)})` : '';
                        const p1FullPosition = p1 ? `${p1.zodiac_position_formatted}${p1HouseInfo}` : a.p1_name;

                        const p2 = planet_positions[a.p2_name];
                        const p2HouseInfo = p2 && !HOUSE_DEFINING_POINTS.includes(a.p2_name) && p2.house != null
                            ? `${p2.house}宮(${formatDegreesMinutesSeconds(p2.hdeg)})` : '';
                        const p2FullPosition = p2 ? `${p2.zodiac_position_formatted}${p2HouseInfo}` : a.p2_name;

                        const aspectType = a.aspect_type ? `${a.aspect_type}` : '';
                        const orbFormatted = formatDegreesMinutesSeconds(a.orb);

                        // 敘述版沒有表格分隔線
                        sectionsData.aspect.narrative += `${a.p1_name}${p1FullPosition}${a.aspect_name}${a.p2_name}${p2FullPosition}，${aspectType}${orbFormatted}。\n`;
                    });
                    sectionsData.aspect.narrative += "====================\n";// 段落間距
                } else {
                    sectionsData.aspect.table = "沒有相位";
                    sectionsData.aspect.narrative = "本命盤中沒有偵測到主要相位。\n";
                }

                return sectionsData;
            }

            function buildSingleChartHTML(sectionsData, title, headerStyleClass = 'single-chart-header-style') {
                if (!sectionsData || !sectionsData.summary) {
                    return `<div class="error-message">${title} 資料缺失或格式不正確。</div>`;
                }

                const { summary, cusp, planet, aspect } = sectionsData;

                return `
        <div class="chart-wrapper">
            <div class="chart-main-header flex items-center justify-between${headerStyleClass}">
                <h2 class="main-title">${title}</h2>
                <div class="flex gap-2">
                <button class="copy-chart-btn">複製此盤</button>
                <button class="download-chart-btn">下載此盤</button>
                </div>
            </div>

            <div class="summary-section-container">
                <div class="result-section-item">
                    ${createResultSection('星盤基礎數據', summary.table, summary.narrative, true, 'summary-header-style')}
                </div>
            </div>

            <div class="sub-sections-container">
                <div class="result-section-item">
                    ${createResultSection('宮頭', cusp.table, cusp.narrative, false, 'cusp-header-style')}
                </div>

                <div class="result-section-item">
                    ${createResultSection('星體位置', planet.table, planet.narrative, false, 'planet-header-style')}
                </div>

                <div class="result-section-item">
                    ${createResultSection('主要相位', aspect.table, aspect.narrative, false, 'aspect-header-style')}
                </div>
            </div>
        </div>`;
            }

            // 新增的輔助函數：生成交互相位部分的數據（表格和敘述兩種格式）
            function generateInterAspectsSectionData(aspects, name1, name2, isTransit = false) {
                const sectionData = { table: '', narrative: '' };
                // 修改後的標題，更具體地指出方向
                const sectionTitle = isTransit ? `${name1}與${name2}` : `${name1}與${name2}`;
                if (!aspects?.length) {
                    sectionData.table = "沒有相位";
                    sectionData.narrative = `雙方之間沒有偵測到${titlePrefix}交互相位。`;
                    return sectionData;
                }

                // --- 表格內容生成 ---
                const tableLines = [
                    // `==== ${sectionTitle} ====`,
                    `\n==== 交互相位：${name1}的星體與${name2}的星體 ====\n`,
                    `${name1}星體 | 相位 | ${name2}星體 | 動態 | 容許度`,
                    "-----------------------------", // 表格分隔線
                    ...aspects.sort((a, b) => DISPLAY_ORDER_NAMES.indexOf(a.p1_name) - DISPLAY_ORDER_NAMES.indexOf(b.p1_name) || DISPLAY_ORDER_NAMES.indexOf(a.p2_name) - DISPLAY_ORDER_NAMES.indexOf(b.p2_name)).map(a =>
                        `${a.p1_name} | ${a.aspect_name} | ${a.p2_name} | ${a.aspect_type || '-'} | ${formatDegreesMinutesSeconds(a.orb)}`
                    ),
                    "===================="
                ];
                sectionData.table = tableLines.join('\n');

                // --- 敘述內容生成 ---
                const narrativeLines = [
                    // "====================",
                    // `${sectionTitle}`,
                    `\n==== 交互相位：${name1}的星體與${name2}的星體 ====\n`,
                    // "--------------------\n" // 【核心修正 2】: 加上換行符，讓分隔線與內容之間多一個空行，更美觀
                ];
                // 假設 planet_positions 在這裡是可以訪問的全局或通過參數傳入，用於獲取更多詳細信息
                // 如果沒有，就只使用 a.p1_name, a.p2_name
                aspects.sort((a, b) => DISPLAY_ORDER_NAMES.indexOf(a.p1_name) - DISPLAY_ORDER_NAMES.indexOf(b.p1_name) || DISPLAY_ORDER_NAMES.indexOf(a.p2_name) - DISPLAY_ORDER_NAMES.indexOf(b.p2_name)).forEach(a => {
                    // 你可以根據需要為敘述版添加更多細節，例如星體所落星座/宮位
                    narrativeLines.push(`${name1}的${a.p1_name}與${name2}的${a.p2_name}形成${a.aspect_name}，容許度為${formatDegreesMinutesSeconds(a.orb)}。`);
                });
                narrativeLines.push("====================");
                sectionData.narrative = narrativeLines.join('\n');

                return sectionData;
            }

            // 修改後的 buildInterAspectsHTML 函數
            // 它現在接收由 generateInterAspectsSectionData 預先生成的內容物件
            function buildInterAspectsHTML(sectionsData, name1, name2, isTransit = false) {
                // 檢查 sectionsData 是否有效
                if (!sectionsData || (typeof sectionsData.table === 'undefined' && typeof sectionsData.narrative === 'undefined')) {
                    return `<div class="error-message">交互相位數據缺失或格式不正確。</div>`;
                }

                const title = isTransit ? `${name1}與${name2}相位` : `交互相位`; // 網頁上顯示的標題

                return `
        <div class="result-section-item">
            ${createResultSection(title, sectionsData.table, sectionsData.narrative, false, 'interaction-header-style')}
        </div>`;
            }

            
            // 新增的輔助函數：生成行星落宮部分的數據（表格和敘述兩種格式）
            function generateOverlaySectionData(overlayData, guestName, hostName, title) {
                const sectionData = { table: '', narrative: '' };
                const dynamicHeaderComment = `${guestName}星體 | 星座度數(度分) | 落入${hostName}宮位(度分)`;

                if (!overlayData?.length) {
                    sectionData.table = "資料缺失";
                    sectionData.narrative = `${title} 的行星落宮資料缺失，無法提供敘述。`;
                    return sectionData;
                }

                // --- 表格內容生成 ---
                const tableLines = [
                    `==== ${title} ====`,
                    dynamicHeaderComment, // 表格標頭
                    "-----------------------------", // 表格分隔線
                    ...overlayData.sort((a, b) => DISPLAY_ORDER_NAMES.indexOf(a.planet_name) - DISPLAY_ORDER_NAMES.indexOf(b.planet_name))
                        .map(o => `${o.planet_name} | ${o.zodiac_position_formatted} | ${o.house_in_target_chart}宮(${formatDegreesMinutesSeconds(o.degree_in_target_house)})`),
                    "====================\n"
                ];
                sectionData.table = tableLines.join('\n');

                // --- 敘述內容生成 ---
                const narrativeLines = [
                    `==== ${title} ====`,
                ];
                overlayData.sort((a, b) => DISPLAY_ORDER_NAMES.indexOf(a.planet_name) - DISPLAY_ORDER_NAMES.indexOf(b.planet_name))
                    .forEach(o => {
                        narrativeLines.push(
                            // 這是行星落宮位元的基本訊息
                            `${guestName}的${o.planet_name}${o.zodiac_position_formatted}落入${hostName}的${o.house_in_target_chart}宮（${formatDegreesMinutesSeconds(o.degree_in_target_house)}）。`
                        );
                        // 🎯 關鍵修改在這裡：添加 o.description 到敘述中
                        // 確保 o.description 存在且有值，如果沒有，就添加一個預設提示或留空
                        if (o.description) {
                            narrativeLines.push(`${o.description}\n`); // 每個描述後面加兩個換行，讓排版更清晰
                        // } else {
                        //     // 如果沒有描述，可以選擇添加一個提示，或者不添加任何內容
                        //     narrativeLines.push(`${o.planet_name}落${o.house_in_target_chart}宮\n`);
                        }
                    });
                narrativeLines.push("===================="); 
                sectionData.narrative = narrativeLines.join('\n');

                return sectionData;
            }

            function buildOverlayHTML(sectionsData, guestName, hostName, title) {
                // 檢查 sectionsData 是否有效
                if (!sectionsData || (typeof sectionsData.table === 'undefined' && typeof sectionsData.narrative === 'undefined')) {
                    return `<div class="error-message">行星落宮資料缺失或格式不正確。</div>`;
                }

                // 🎯 這裡，讓它直接使用別人給它的 `title`
                const displayTitle = title;

                return `
    <div class="result-section-item">
        ${createResultSection(displayTitle, sectionsData.table, sectionsData.narrative, false, 'interaction-header-style')}
    </div>`;
            }

            function createResultSection(title, tableContent, narrativeContent, isSummary = false, headerStyleClass = '') {
                // 根據你的要求：所有章節（包括 summary）都需要有複製按鈕。
                // 所以 copyButtonHtml 無條件地生成按鈕的 HTML 字串。
                const copyButtonHtml = `<button class="section-copy-btn">複製</button>`;

                // sectionHeaderClass 仍根據 isSummary 判斷，用於樣式區分 (summary-header-style vs. result-section-header)。
                const sectionHeaderClass = isSummary ? 'summary-section-header' : 'result-section-header';

                return `
        <div class="${sectionHeaderClass} ${headerStyleClass}">
            <h3>${title}</h3>
            ${copyButtonHtml}
        </div>
        <div class="result-section-content scrollable-content">
            <pre class="table-content">${tableContent}</pre>
            <pre class="narrative-content" style="display:none;">${narrativeContent}</pre>
        </div>
    `;
            }
            
            // 這是一個全新的函式，請將它新增到 script 中
            function createReportWrapper(title, content) {
                return `<div class="report-wrapper">
                <div class="report-main-header flex items-center justify-between">
                      <h2 class="main-title">${title}</h2>
                      <div class="flex gap-2">
                          <button class="copy-report-btn">複製完整報告</button>
                          <button class="download-report-btn">下載完整報告</button>
                       </div>
                </div>
                ${content}
            </div>`;
            }
            // 執行初始化
            initializeApp();
        });
    