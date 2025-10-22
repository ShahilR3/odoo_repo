import publicWidget from "@web/legacy/js/public/public_widget";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.PropertyCarousel = publicWidget.Widget.extend({
    selector: '.mySwiper',
    async start() {
        const container = this.$el.find('.swiper-wrapper');
        try {
            const properties = await rpc('/property/list/json', {});
            for (const property of properties) {
                const slideHtml = `
                    <div class="swiper-slide property-card">
                        <a href="/property/details/${property.id}">
                           <div class="card">
                              <img src="${property.image}" class="card-img-top" alt="${property.name}" style="height: 200px; object-fit: cover; width: 100%;" />
                              <div class="card-body">
                                <h5 class="card-title">${property.name}</h5>
                                <p class="card-text">Price: ${property.currency}${property.legal_amount}</p>
                              </div>
                           </div>
                        </a>
                    </div>
                `;
                container.append(slideHtml);
            }
            const shouldLoop = properties.length > 4;
            new Swiper(this.el, {
                slidesPerView: 4,
                slidesPerGroup: 4,
                spaceBetween: 20,
                loop: shouldLoop,
                autoplay: {
                    delay: 3000,
                    disableOnInteraction: false,
                },
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
            });
        } catch (error) {
            console.error('Failed to load property carousel:', error);
        }
    }
});
