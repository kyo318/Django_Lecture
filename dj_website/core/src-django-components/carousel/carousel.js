(function () {
  observeNodeInsertion(".carousel-component", (el) => {
    const carousel = new bootstrap.Carousel(el);

    let mouseStartX = 0;
    let mouseStartY = 0;

    el.addEventListener("mousedown", (e) => {
      mouseStartX = e.screenX;
      mouseStartY = e.screenY;
    });

    el.addEventListener("mouseup", (e) => {
      const mouseEndX = e.screenX;
      const mouseEndY = e.screenY;

      const deltaX = Math.abs(mouseEndX - mouseStartX);
      const deltaY = Math.abs(mouseEndY - mouseStartY);

      if (deltaX > deltaY) {
        if (mouseStartX > mouseEndX) carousel.next();
        else if (mouseStartX < mouseEndX) carousel.prev();
      }
    });
  });
})();
