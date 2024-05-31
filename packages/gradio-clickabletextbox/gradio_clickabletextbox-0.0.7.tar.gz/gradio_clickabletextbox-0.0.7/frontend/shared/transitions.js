// transitions.js
import { cubicOut } from 'svelte/easing';

export function fadeSlide(node, { delay = 0, duration = 500, easing = cubicOut } = {}) {
    const height = parseFloat(getComputedStyle(node).height);

    return {
        delay,
        duration,
        easing,
        css: t => {
            const opacity = t;
            const transform = `translateY(${(1 - t) * -10}px)`;
            const currentHeight = t * height;
            return `
                opacity: ${opacity};
                transform: ${transform};
                height: ${currentHeight}px;
            `;
        }
    };
}
