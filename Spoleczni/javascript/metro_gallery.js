/**
|------------------------------------------|
| MelonHTML5 - Metro Gallery               |
|------------------------------------------|
| @author:  Lee Le (lee@melonhtml5.com)    |
| @version: 1.12 (30 Aug 2014)             |
| @website: www.melonhtml5.com             |
|------------------------------------------|
*/

// shim layer with setTimeout fallback
window.requestAnimFrame = (function() {
    return window.requestAnimationFrame       ||
           window.webkitRequestAnimationFrame ||
           window.mozRequestAnimationFrame    ||
           window.oRequestAnimationFrame      ||
           window.msRequestAnimationFrame     ||
           function(callback) {
               window.setTimeout(callback, 1000 / 60);
           };
})();

var Metro_Gallery = {
    _containers:    null,
    _tiles:         null,
    _images:        [],

    _image_pointer: 0,

    _lightbox:      null,
    _overlay:       null,

    _loaded:        false,

    _configs: {
        base_size:  100,
        gutter:     10,
        scale:      1.4,
        delay:      1000
    },

    _can_flip: false,
    _use_css_animation: true,

    _css3SupportDetect: function() {
        var style = document.body.style;

        if (typeof style['transition'] == 'string') {
            Metro_Gallery._use_css_animation = true;
            return true;
        }

        // Tests for vendor specific prop
        var prefix = ['Webkit', 'Moz', 'Khtml', 'O', 'ms'];
        for (var i=0; i< prefix.length; i++) {
            if (typeof (style[prefix[i] + 'Transition']) == 'string') {
                Metro_Gallery._use_css_animation = true;
                return true;
            }
        }

        Metro_Gallery._use_css_animation = false;
        return false;
    },

    _transitionEnd: function(element, event_handler) {
        if (Metro_Gallery._use_css_animation) {
            transEndEventNames = 'webkitTransitionEnd oTransitionEnd MSTransitionEnd transitionend';

            element.on(transEndEventNames, function (event) {
                element.off(transEndEventNames);
                event_handler(event, element);
            });
        } else {
            event_handler(null, element);
        }

        // return element so that we can chain methods
        return element;
    },

    _init: function() {
        Metro_Gallery._css3SupportDetect();

        $(document.body).addClass('loaded');
        Metro_Gallery._cache_elements();

        Metro_Gallery._buildStyles();
        Metro_Gallery._build();
    },

    _start: function() {
        if (Metro_Gallery._loaded) {
            return;
        }

        var column_width = Metro_Gallery._configs.base_size + Metro_Gallery._configs.gutter;

        var first_tile = Metro_Gallery._tiles.eq(0);
        var classes = first_tile.attr('class').split(' ');
        $(classes).each(function(index, class_name) {
            if (class_name.indexOf('tile_') !== -1) {
                // 'tile_2x2'
                // width = size * 1x1_width + (size - 1) x 2 x margin
                var size      = class_name.replace(/tile_/, '').substr(0, 1);
                var margin    = parseInt(first_tile.css('margin-right'), 10);
                var width_1x1 = (first_tile.width() + 2 * margin - 2 * margin * size) / size;

                column_width = width_1x1 + 2 * margin;

                return false;
            }
        });

        Metro_Gallery._containers.each(function() {
            var container  = $(this);
            var directions = ['up', ''];

            if (!container.hasClass('vertical') && !container.hasClass('horizontal')) {
                container.addClass('vertical');
            }

            var msnry = new Masonry(container.get(0), {
                itemSelector :      '.tile',
                columnWidth  :      column_width,
                transitionDuration: '0.7s'
            });
            container.data('msnry', msnry);
        });

        Metro_Gallery._tiles.each(function(index) {
            var tile = $(this);

            setTimeout(function() {
                if (Metro_Gallery._use_css_animation) {
                    Metro_Gallery._transitionEnd(tile, function(evt, element) {
                        element.removeClass('animating');
                    }).addClass('animating loaded');
                } else {
                    var container = tile.parents('.metro_gallery');

                    if (container.hasClass('fade') || container.hasClass('flip') || container.hasClass('scale')) {
                        tile.animate({opacity:1}, 200, 'linear', function() {
                            tile.addClass('loaded');
                        })
                    } else {
                        tile.addClass('loaded');
                    }
                }
            }, index * 100);

            tile.mouseenter(Metro_Gallery.Events.onMouseEnter).mouseleave(Metro_Gallery.Events.onMouseLeave);
        });

        Metro_Gallery._images.each(function(index) {
            $(this).data('index', index);
        });

        $(document).keyup(Metro_Gallery.Events.onKeyUp);

        // swipe
        if (typeof Hammer !== 'undefined') {
            try {
                var hammertime = Hammer(document.body, {swipe_velocity: 0.2}).on('swipeleft',  Metro_Gallery.Events.onSwipeLeft);
                var hammertime = Hammer(document.body, {swipe_velocity: 0.2}).on('swiperight', Metro_Gallery.Events.onSwipeRight);
            } catch(e) {
            }
        }

        if (Metro_Gallery._can_flip) {
            setTimeout(function() {
                Metro_Gallery._startFlip();
            }, (Metro_Gallery._tiles.length - 1) * 100 + 200);
        }

        Metro_Gallery._loaded = true;
    },

    _cache_elements: function() {
        this._tiles      = $('div.tile');
        this._containers = $('.metro_gallery');
        this._images     = $('div.tile').children('img');
    },

    _buildStyles: function() {
        var styles = '';
        var crlf   = '\r\n';

        var width_increase = (Metro_Gallery._configs.scale - 1) * Metro_Gallery._configs.base_size;

        styles += 'div.tile {';
        styles +=     'margin: ' + Metro_Gallery._configs.gutter / 2 + 'px;';
        styles += '}';

        for (var x = 1; x <= 10; x++) {
            for (y = 1; y <= 10; y++) {
                var width  = x * Metro_Gallery._configs.base_size + (x - 1) * Metro_Gallery._configs.gutter;
                var height = y * Metro_Gallery._configs.base_size + (y - 1) * Metro_Gallery._configs.gutter;

                styles += 'div.tile_'+ x +'x' +  y + ' {' + crlf;
                styles +=     'width: ' + width + 'px;' + crlf;
                styles +=     'height: ' + height + 'px;' + crlf;
                styles += '}' + crlf;
                styles += 'div.tile_' +  x + 'x' + y + ':hover {' + crlf;
                styles +=     'width: ' + (width + width_increase) + 'px;' + crlf;
                styles +=     'height: ' + (height * (width + width_increase) / width) + 'px;' + crlf;
                styles +=     'margin-top: ' + (Metro_Gallery._configs.gutter / 2 - parseInt((((height * (width + width_increase) / width) - height) / 2), 10)) + 'px;' + crlf;
                styles +=     'margin-left: ' + (Metro_Gallery._configs.gutter / 2 - parseInt((width_increase / 2), 10)) + 'px;' + crlf;
                styles += '}' + crlf;
            }
        }

        $('<style type="text/css">'+styles+'</style>').appendTo($('head'));
    },

    _build: function() {
        Metro_Gallery._tiles.each(function(index) {
            var tile          = $(this);
            var container     = tile.parent();
            var images        = tile.children('img,div');
            var img_container = $('<div>').addClass('img_container');
            var scroller      = $('<div>').addClass('scroller').append(images).appendTo(img_container);
            var caption       = $('<div>').addClass('caption');

            if (images.eq(0).data('caption')) {
                if (images.eq(0).data('captionlink')) {
                    caption.html('<a href="' + images.eq(0).data('captionlink') + '">' + images.eq(0).data('caption') + '</a>');
                } else {
                    caption.text(images.eq(0).data('caption'));
                }

                tile.addClass('caption');
            }

            if (container.hasClass('vertical')) {
                scroller.height(images.length * 100 + '%');
                images.height(100 / images.length + '%');
            } else {
                scroller.width(images.length * 100 + '%');
                images.width(100 / images.length + '%');
            }

            tile.data({
                active:       1,
                num_images:   images.length,
                caption:      caption,
                scroller:     scroller
            }).append(img_container).append(caption);

            images.click(Metro_Gallery.Events.imageClick);

            if (images.length > 1) {
                var prev = $('<a>').attr('href', '#').addClass('prev').data('tile', tile).click(Metro_Gallery.Events.prevClick);
                var next = $('<a>').attr('href', '#').addClass('next').data('tile', tile).click(Metro_Gallery.Events.nextClick);

                tile.append(prev).append(next).data('prev', prev).data('next', next);

                Metro_Gallery._can_flip = true;
            }
        });
    },

    _startFlip: function() {
        setInterval(function() {
            var random_tile = false;
            var counter = 0;
            while (!random_tile) {
                counter++;
                if (counter >= 10) {
                    break;
                }

                random_tile = Metro_Gallery._tiles.eq(Math.floor((Math.random() * Metro_Gallery._tiles.length)));
                if (random_tile.data('num_images') <= 1 || random_tile.data('hover')) {
                    random_tile = false;
                }
            }

            if (random_tile) {
                random_tile.data('next').click();
            }
        }, Metro_Gallery._configs.delay);
    },

    _goNext: function(tile, direction) {
        var container = tile.parent();
        var scroller  = tile.data('scroller');
        var active    = tile.data('active');
        var num       = tile.data('num_images');
        var next      = direction === 'next' ? (active === num ? 1 : active + 1) : (active === 1 ? num : active - 1);
        var image     = scroller.children('img,div').eq(next - 1);

        if (image.data('caption')) {
            if (image.data('captionlink')) {
                tile.data('caption').html('<a href="' + image.data('captionlink') + '">' + image.data('caption') + '</a>');
            } else {
                tile.data('caption').text(image.data('caption'));
            }

            tile.addClass('caption');
            tile.data('caption').text(image.data('caption'));
        } else {
            tile.removeClass('caption');
            tile.data('caption').text('');
        }

        var transition_property = container.hasClass('vertical') ? 'top' : 'left';

        if (this._use_css_animation) {
            scroller.css(transition_property, (next - 1) * -100 + '%');
        } else {
            if (transition_property === 'top') {
                scroller.animate({top: (next - 1) * -100 + '%'}, 200);
            } else {
                scroller.animate({left: (next - 1) * -100 + '%'}, 200);
            }
        }

        tile.data('active', next);

        if (direction === 'next') {
            if (next > 1) {
                tile.data('prev').show();
            } else {
                tile.data('prev').hide();
            }

            if (next === num) {
                tile.data('next').hide();
            } else {
                tile.data('next').show();
            }
        } else {
            if (next === 1) {
                tile.data('prev').hide();
            } else {
                tile.data('prev').show();
            }

            if (next < num) {
                tile.data('next').show();
            } else {
                tile.data('next').hide();
            }
        }
    },

    _closeLightbox: function(e) {
        if (Metro_Gallery._use_css_animation) {
            Metro_Gallery._overlay.removeClass('open');
            Metro_Gallery._lightbox.addClass('close');
        } else {
            Metro_Gallery._overlay.animate({opacity:0}, 200);
            Metro_Gallery._lightbox.animate({opacity:0, top:'48%'}, 400);
        }

        setTimeout(function() {
            Metro_Gallery._overlay.remove();
            Metro_Gallery._overlay = null;
        }, 200);

        setTimeout(function() {
            Metro_Gallery._lightbox.remove();
            Metro_Gallery._lightbox = null;
        }, 400);
    },

    _openLightbox: function(img) {
        var tile = img.parents('div.tile:first');
        var container = tile.parent();

        if (!Metro_Gallery._overlay) {
            Metro_Gallery._overlay = $('<div>').addClass('metro_overlay').click(Metro_Gallery._closeLightbox).appendTo($(document.body));

            if (Metro_Gallery._use_css_animation) {
                requestAnimFrame(function() {
                    Metro_Gallery._overlay.addClass('open');
                });
            } else {
                Metro_Gallery._overlay.animate({opacity:0.6}, 200, null, function() {
                    Metro_Gallery._overlay.addClass('open');
                });
            }
        }

        var is_video = img.data('iframe') ? true : false;

        if (is_video) {
            var url = img.data('iframe');
            if (url.indexOf('?')) {
                img.data('iframe', url + '&wmode=opaque');
            } else {
                img.data('iframe', url + '?wmode=opaque');
            }
        }

        var _buildLightbox = function(width, height) {
            var size = Metro_Gallery._getLightboxSize(width, height);
            var new_css = {
                'margin':       '-' + size.height / 2 + 'px 0px 0px -' + size.width / 2 + 'px',
                'border-color': tile.css('background-color'),
                'width':        size.width,
                'height':       size.height
            };

            var do_append = false;
            var new_img = false;

            if (!Metro_Gallery._lightbox) {
                do_append = true;

                Metro_Gallery._lightbox = $('<div>').addClass('metro_lightbox').css(new_css);

                if (is_video) {
                    new_img = $('<iframe>').attr('src', img.data('iframe')).attr('width', Math.ceil(size.width)).attr('height', Math.ceil(size.height)).attr('frameborder', '0').appendTo(Metro_Gallery._lightbox);
                } else {
                    new_img = $('<img>').attr('src', img.data('preview') ? img.data('preview') : img.attr('src')).width(Math.ceil(size.width)).height(Math.ceil(size.height)).appendTo(Metro_Gallery._lightbox);
                }

                var prev    = $('<a>').attr('href', '#').addClass('prev').click(Metro_Gallery.Events.lightboxPrevClick).appendTo(Metro_Gallery._lightbox);
                var next    = $('<a>').attr('href', '#').addClass('next').click(Metro_Gallery.Events.lightboxNextClick).appendTo(Metro_Gallery._lightbox);

                if (img.data('caption')) {
                    if (img.data('captionlink')) {
                        $('<div>').addClass('caption').html('<a href="' + img.data('captionlink') + '">' + img.data('caption') + '</a>').appendTo(Metro_Gallery._lightbox);
                    } else {
                        $('<div>').addClass('caption').text(img.data('caption')).appendTo(Metro_Gallery._lightbox);
                    }
                }
            } else {
                Metro_Gallery._lightbox.children('iframe').remove();
                Metro_Gallery._lightbox.children('img').remove();

                Metro_Gallery._lightbox.addClass('change');


                if (Metro_Gallery._use_css_animation) {
                    Metro_Gallery._lightbox.css(new_css);
                } else {
                    Metro_Gallery._lightbox.animate(new_css, 700);
                }

                if (is_video) {
                    new_img = $('<iframe>').attr('src', img.data('iframe')).attr('width', Math.ceil(size.width)).attr('height', Math.ceil(size.height)).attr('frameborder', '0').appendTo(Metro_Gallery._lightbox);
                } else {
                    new_img = $('<img>').attr('src', img.data('preview') ? img.data('preview') : img.attr('src')).width(Math.ceil(size.width)).height(Math.ceil(size.height)).appendTo(Metro_Gallery._lightbox);
                }

                if (img.data('caption')) {
                    if (img.data('captionlink')) {
                        Metro_Gallery._lightbox.children('div.caption').html('<a href="' + img.data('captionlink') + '">' + img.data('caption') + '</a>').show();
                    } else {
                        Metro_Gallery._lightbox.children('div.caption').text(img.data('caption')).show();
                    }
                } else {
                    Metro_Gallery._lightbox.children('div.caption').hide();
                }

                setTimeout(function() {
                    Metro_Gallery._lightbox.removeClass('change');

                    if (!Metro_Gallery._use_css_animation && new_img) {
                        new_img.hide();
                        setTimeout(function() {
                            new_img.fadeIn();
                        }, 700);
                    }
                }, 200);
            }

            if (do_append) {
                Metro_Gallery._lightbox.appendTo($(document.body));

                if (Metro_Gallery._use_css_animation) {
                    // force page reflow
                    $(window).width();

                    requestAnimFrame(function() {
                        Metro_Gallery._lightbox.addClass('open');
                    });
                } else {
                    Metro_Gallery._lightbox.animate({top:'50%'}, 700, null, function() {
                        Metro_Gallery._lightbox.addClass('open');
                    });
                }
            }
        };

        if (is_video) {
            _buildLightbox(img.data('iframewidth'), img.data('iframeheight'));
        } else {
            var img_element = new Image();
            img_element.src = img.data('preview') ? img.data('preview') : img.attr('src');

            if (img_element.complete) {
                _buildLightbox(img_element.width, img_element.height);
            } else {
                img_element.onload = function() {
                    _buildLightbox(this.width, this.height);
                };
            }
        }
    },

    _getLightboxSize: function(width, height) {
        var max_width  = $(window).width() * 0.8;
        var max_height = $(window).height() * 0.8;

        var new_width  = width;
        var new_height = height;

        if (width > max_width || height > max_height) {
            var ratio = width / height;

            if (width > max_width && height <= max_height) {
                new_width  = max_width;
                new_height = height / (width / new_width);
            } else if (height > max_height && width <= max_width) {
                new_height = max_height;
                new_width  = width / (height / new_height);
            } else {
                new_width  = max_width;
                new_height = height / (width / new_width);

                if (new_height > max_height) {
                    new_height = max_height;
                    new_width  = width / (height / new_height);
                }
            }
        }

        return {width:new_width, height:new_height};
    },

    setOptions: function(opts) {
        Metro_Gallery._configs.base_size  = typeof opts.base_size  !== 'undefined' ? parseInt(opts.base_size, 10) : Metro_Gallery._configs.base_size;
        Metro_Gallery._configs.gutter     = typeof opts.gutter     !== 'undefined' ? parseInt(opts.gutter, 10)    : Metro_Gallery._configs.gutter;
        Metro_Gallery._configs.scale      = typeof opts.scale      !== 'undefined' ? parseFloat(opts.scale)       : Metro_Gallery._configs.scale;
        Metro_Gallery._configs.delay      = typeof opts.delay      !== 'undefined' ? parseInt(opts.delay, 10)     : Metro_Gallery._configs.delay;
    },

    Events: {
        onMouseEnter: function(e) {
            $(this).data('hover', true);
        },

        onMouseLeave: function(e) {
            $(this).data('hover', false);
        },

        onKeyUp: function(e) {
            if (Metro_Gallery._lightbox) {
                switch (e.which) {
                    case 27: // ESC
                        Metro_Gallery._closeLightbox(e);
                        break;
                    case 37: // LEFT
                        Metro_Gallery.Events.lightboxPrevClick(e);
                        break;
                    case 39: // RIGHT
                        Metro_Gallery.Events.lightboxNextClick(e);
                        break;
                }

            }
        },

        prevClick: function(e) {
            e.preventDefault();
            e.stopPropagation();
            Metro_Gallery._goNext($(this).data('tile'), 'back');
        },

        nextClick: function(e) {
            e.preventDefault();
            e.stopPropagation();
            Metro_Gallery._goNext($(this).data('tile'), 'next');
        },

        lightboxPrevClick: function(e) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }

            if (Metro_Gallery._image_pointer === 0) {
                Metro_Gallery._image_pointer = Metro_Gallery._images.length - 1;
            } else {
                Metro_Gallery._image_pointer--;
            }

            Metro_Gallery._images.eq(Metro_Gallery._image_pointer).click();
        },

        lightboxNextClick: function(e) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }

            if (Metro_Gallery._image_pointer === Metro_Gallery._images.length - 1) {
                Metro_Gallery._image_pointer = 0;
            } else {
                Metro_Gallery._image_pointer++;
            }

            Metro_Gallery._images.eq(Metro_Gallery._image_pointer).click();
        },

        imageClick: function(e) {
            e.stopPropagation();

            var image_clicked = $(this);
            var link          = image_clicked.data('link');

            if (image_clicked.prop('tagName').toLowerCase() !== 'img') {
                return;
            }

            if (link) {
                window.open(link, '_blank');
            } else {
                var container = image_clicked.parents('.metro_gallery');
                if (container.hasClass('lightbox')) {
                    // set pointer
                    Metro_Gallery._images.each(function(index) {
                        if ($(this).get(0) === image_clicked.get(0)) {
                            Metro_Gallery._image_pointer = index;
                            return false;
                        }
                    });

                    Metro_Gallery._openLightbox(image_clicked);
                }
            }
        },

        onSwipeLeft: function(e) {
            if (Metro_Gallery._overlay && Metro_Gallery._lightbox) {
                Metro_Gallery.Events.lightboxPrevClick();
            }
        },

        onSwipeRight: function(e) {
            if (Metro_Gallery._overlay && Metro_Gallery._lightbox) {
                Metro_Gallery.Events.lightboxNextClick();
            }
        }
    }
};


$(document).ready(Metro_Gallery._init);

setTimeout(Metro_Gallery._start, 5000);
$(window).load(Metro_Gallery._start);