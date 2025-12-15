// static/js/cart.js
document.addEventListener('DOMContentLoaded', () => {
  // Удобные селекты
  const qtyInputs = Array.from(document.querySelectorAll('.js-qty'));
  const deliveryRadios = Array.from(document.querySelectorAll('.js-delivery'));
  const subtotalEl = document.getElementById('cart-subtotal');
  const deliveryEl = document.getElementById('cart-delivery');
  const totalEl = document.getElementById('cart-total');
  const checkoutBtn = document.getElementById('checkout-button');

  // modal
  const modal = document.getElementById('order-modal');
  const modalOk = document.getElementById('order-modal-ok');

  // helper to parse price text to number
  function parsePrice(v) {
    if (v === null || v === undefined) return 0;
    return Number(String(v).replace(/\s+/g, '').replace(',', '.')) || 0;
  }

  function formatPrice(n) {
    // без валюты, ты можешь добавить ₽ в шаблоне
    return parseFloat(n).toFixed(2).replace('.00', '');
  }

  function recalcLine(input) {
    const li = input.closest('.cart-cards_item');
    if (!li) return 0;
    const priceEl = li.querySelector('.cart-card__price');
    const lineEl = li.querySelector('.js-line-total');
    const price = parsePrice(priceEl.dataset.price || priceEl.textContent);
    const qty = Math.max(1, parseInt(input.value) || 1);
    const line = price * qty;
    if (lineEl) lineEl.textContent = formatPrice(line);
    return line;
  }

  function recalcSubtotal() {
    // суммируем все line totals из DOM
    const lineEls = Array.from(document.querySelectorAll('.js-line-total'));
    const subtotal = lineEls.reduce((s, el) => s + parsePrice(el.textContent), 0);
    if (subtotalEl) subtotalEl.textContent = formatPrice(subtotal);
    return subtotal;
  }

  function getSelectedDeliveryCost() {
    const sel = deliveryRadios.find(r => r.checked);
    if (!sel) return 0;
    return parseFloat(sel.dataset.cost || 0) || 0;
  }

  function updateTotals() {
    const subtotal = recalcSubtotal();
    const delivery = getSelectedDeliveryCost();
    if (deliveryEl) deliveryEl.textContent = formatPrice(delivery);
    if (totalEl) totalEl.textContent = formatPrice(subtotal + delivery);
  }

  // Событие: изменение количества
  qtyInputs.forEach(inp => {
    inp.addEventListener('change', async (e) => {
      const newQty = Math.max(1, parseInt(inp.value) || 1);
      inp.value = newQty;
      // пересчёт в DOM
      recalcLine(inp);
      updateTotals();

      // Опционально: отправить на сервер, чтобы синхронизировать с сессией
      // отправляем POST /cart/update/ с product_id и qty (если у тебя есть view)
      const pid = inp.dataset.productId;
      if (pid) {
        try {
          await fetch('/cart/update/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-CSRFToken': getCookie('csrftoken'),
            },
            body: `product_id=${encodeURIComponent(pid)}&qty=${encodeURIComponent(newQty)}`
          });
        } catch (err) { /* ignore network errors for now */ }
      }
    });
  });

  // Событие: смена способа доставки
  deliveryRadios.forEach(r => {
    r.addEventListener('change', () => {
      updateTotals();
    });
  });

  // Checkout click
  checkoutBtn && checkoutBtn.addEventListener('click', (e) => {
    // Если хотите — здесь можно сделать валидацию полей доставки
    // Показать модалку
    if (modal) {
      modal.style.display = 'block';
      modal.setAttribute('aria-hidden', 'false');
    }
  });

  // modal OK
  modalOk && modalOk.addEventListener('click', () => {
    if (modal) {
      modal.style.display = 'none';
      modal.setAttribute('aria-hidden', 'true');
    }
    // Можно отправить POST для создания реального заказа здесь
    // fetch('/orders/create/', { method: 'POST', ... })
  });

  // helper: get CSRF cookie
  function getCookie(name) {
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? v.pop() : '';
  }

  // initial
  updateTotals();
});
