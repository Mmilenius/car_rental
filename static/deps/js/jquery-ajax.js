// ==========================================
// 1. ЛОГІКА КОШИКА ТА ОБРАНОГО (jQuery)
// ==========================================
$(document).ready(function () {
    var successMessage = $("#jq-notification");

    // Універсальна функція оновлення кошика
    function updateCart(cartID, period, changeUrl) {
        $.ajax({
            type: "POST",
            url: changeUrl,
            data: {
                cart_id: cartID,
                period: period,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                if (successMessage.length > 0) {
                    successMessage.find('.message-text').text(data.message);
                    successMessage.removeClass('hidden translate-x-full opacity-0');
                    setTimeout(function () {
                        successMessage.addClass('translate-x-full opacity-0');
                        setTimeout(() => successMessage.addClass('hidden'), 300);
                    }, 3000);
                }

                $("#cart-items-container").html(data.cart_items_html);

                if (data.total_quantity !== undefined) {
                    $("#cars-in-cart-count").text(data.total_quantity);
                }
            },
            error: function (data) {
                console.log("Помилка при оновленні кошика");
            },
        });
    }

    // Додавання в кошик
    $(document).off("click", ".add-to-cart").on("click", ".add-to-cart", function (e) {
        e.preventDefault();
        var car_id = $(this).data("car-id");
        var add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                car_id: car_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                if (successMessage.length > 0) {
                    successMessage.find('.message-text').text(data.message);
                    successMessage.removeClass('hidden translate-x-full opacity-0');
                    setTimeout(function () {
                        successMessage.addClass('translate-x-full opacity-0');
                        setTimeout(() => successMessage.addClass('hidden'), 300);
                    }, 3000);
                }
                $("#cart-items-container").html(data.cart_items_html);
                if (data.total_quantity !== undefined) {
                    $("#cars-in-cart-count").text(data.total_quantity);
                }
            },
            error: function (data) {
                console.log("Помилка при додаванні");
            },
        });
    });

    // Видалення з кошика
    $(document).off("click", ".remove-from-cart").on("click", ".remove-from-cart", function (e) {
        e.preventDefault();
        var cart_id = $(this).data("cart-id");
        var remove_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: remove_url,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                $("#cart-items-container").html(data.cart_items_html);
                if (data.total_quantity !== undefined) {
                    $("#cars-in-cart-count").text(data.total_quantity);
                }
            },
            error: function (data) {
                console.log("Помилка при видаленні");
            },
        });
    });

    // Кнопка МІНУС
    $(document).on("click", ".decrement-btn", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).siblings(".cart-qty-input");
        var currentVal = parseInt($input.val());

        if (currentVal > 1) {
            $input.val(currentVal - 1);
            updateCart(cartID, currentVal - 1, url);
        }
    });

    // Кнопка ПЛЮС
    $(document).on("click", ".increment-btn", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).siblings(".cart-qty-input");
        var currentVal = parseInt($input.val());

        $input.val(currentVal + 1);
        updateCart(cartID, currentVal + 1, url);
    });

    // Ручне введення кількості
    $(document).on("change", ".cart-qty-input", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var val = parseInt($(this).val());

        if (isNaN(val) || val < 1) {
            val = 1;
            $(this).val(1);
        }
        updateCart(cartID, val, url);
    });

    // Блокування Enter у інпуті
    $(document).on("keypress", ".cart-qty-input", function (e) {
        if (e.which === 13) {
            e.preventDefault();
            $(this).blur();
        }
    });

    // Додавання/Видалення з ОБРАНОГО
    $(document).on("click", ".add-to-favorites", function (e) {
        e.preventDefault();
        var btn = $(this);
        var carId = btn.data("car-id");
        var url = btn.data("url");
        var icon = btn.find("svg");

        $.ajax({
            type: "POST",
            url: url,
            data: {
                car_id: carId,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                if (data.is_favorited) {
                    icon.removeClass("text-gray-400").addClass("text-red-500 fill-current");
                } else {
                    icon.removeClass("text-red-500 fill-current").addClass("text-gray-400");
                }

                var counter = $("#favorites-count");
                counter.text(data.favorites_count);

                if (data.favorites_count > 0) {
                    counter.removeClass("hidden");
                } else {
                    counter.addClass("hidden");
                }

                if (successMessage.length > 0) {
                    successMessage.find('.message-text').text(data.message);
                    successMessage.removeClass('hidden translate-x-full opacity-0');
                    setTimeout(function () {
                        successMessage.addClass('translate-x-full opacity-0');
                        setTimeout(() => successMessage.addClass('hidden'), 300);
                    }, 2000);
                }
            },
            error: function (xhr) {
                if (xhr.status === 403 || xhr.status === 401) {
                    window.location.href = "/users/login/";
                } else {
                    console.log("Помилка додавання в обране");
                }
            }
        });
    });
});

// ==========================================
// 2. ЛОГІКА AI-ЧАТУ (Vanilla JS + jQuery Ajax)
// ==========================================
document.addEventListener("DOMContentLoaded", function () {
    const chatToggle = document.getElementById("ai-chat-toggle");
    const chatWindow = document.getElementById("ai-chat-window");
    const chatClose = document.getElementById("ai-chat-close");
    const chatForm = document.getElementById("ai-chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatMessages = document.getElementById("chat-messages");
    const imageInput = document.getElementById("chat-image-input");
    const imagePreviewContainer = document.getElementById("image-preview-container");
    const imagePreview = document.getElementById("image-preview");
    const removeImageBtn = document.getElementById("remove-image");
    const sendBtn = document.getElementById("send-btn");

    // Якщо елементів чату немає на сторінці (наприклад, адмінка), виходимо
    if (!chatToggle) return;

    function toggleChat() {
        if (chatWindow.classList.contains("hidden")) {
            chatWindow.classList.remove("hidden");
            setTimeout(() => {
                chatWindow.classList.remove("scale-95", "opacity-0");
                chatWindow.classList.add("scale-100", "opacity-100");
            }, 10);
        } else {
            chatWindow.classList.remove("scale-100", "opacity-100");
            chatWindow.classList.add("scale-95", "opacity-0");
            setTimeout(() => {
                chatWindow.classList.add("hidden");
            }, 300);
        }
    }

    chatToggle.addEventListener("click", toggleChat);
    chatClose.addEventListener("click", toggleChat);

    imageInput.addEventListener("change", function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                imagePreviewContainer.classList.remove("hidden");
            }
            reader.readAsDataURL(file);
        }
    });

    removeImageBtn.addEventListener("click", function() {
        imageInput.value = "";
        imagePreviewContainer.classList.add("hidden");
    });

    function appendMessage(sender, text, isImage = false) {
        const div = document.createElement("div");
        div.className = sender === "user" ? "flex gap-2 justify-end" : "flex gap-2";

        let content = '';
        if (sender === "user") {
            content = `
                <div class="bg-blue-600 text-white p-3 rounded-2xl rounded-tr-none shadow-md max-w-[80%] text-left">
                    ${isImage ? '<span class="text-xs opacity-75 block mb-1">📷 Фото додано</span>' : ''}
                    ${text}
                </div>
            `;
        } else {
            content = `
                <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0 text-blue-600">🤖</div>
                <div class="bg-white p-3 rounded-2xl rounded-tl-none shadow-sm border border-gray-100 text-zinc-700 max-w-[85%] prose prose-sm">
                    ${text}
                </div>
            `;
        }

        div.innerHTML = content;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTyping() {
        const div = document.createElement("div");
        div.id = "typing-indicator";
        div.className = "flex gap-2";
        div.innerHTML = `
            <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0 text-blue-600">🤖</div>
            <div class="bg-white p-4 rounded-2xl rounded-tl-none shadow-sm border border-gray-100 flex gap-1 items-center h-10">
                <div class="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
            </div>
        `;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTyping() {
        const indicator = document.getElementById("typing-indicator");
        if (indicator) indicator.remove();
    }

    chatForm.addEventListener("submit", function(e) {
        e.preventDefault();

        const message = chatInput.value.trim();
        const hasImage = imageInput.files.length > 0;

        if (!message && !hasImage) return;

        appendMessage("user", message || "Фото автомобіля", hasImage);

        chatInput.value = "";
        imageInput.value = "";
        imagePreviewContainer.classList.add("hidden");

        showTyping();
        sendBtn.disabled = true;

        const formData = new FormData(this);
        if (!message) formData.set("message", "Підбери авто по цьому фото");

        // ТУТ ГОЛОВНА ЗМІНА: беремо URL з атрибута action форми
        // Це дозволяє тримати JS у статичному файлі
        const ajaxUrl = this.getAttribute("action");

        $.ajax({
            url: ajaxUrl,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                removeTyping();
                sendBtn.disabled = false;
                appendMessage("ai", response.answer);
            },
            error: function() {
                removeTyping();
                sendBtn.disabled = false;
                appendMessage("ai", "Щось пішло не так. Спробуйте ще раз.");
            }
        });
    });

    chatInput.addEventListener("keydown", function(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event("submit"));
        }
    });
});