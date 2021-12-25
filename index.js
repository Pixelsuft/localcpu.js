const {
  createCanvas
} = require('canvas');
const v86 = require('./build/libv86.js');


const charmap_high = new Uint16Array([
  0xC7, 0xFC, 0xE9, 0xE2, 0xE4, 0xE0, 0xE5, 0xE7,
  0xEA, 0xEB, 0xE8, 0xEF, 0xEE, 0xEC, 0xC4, 0xC5,
  0xC9, 0xE6, 0xC6, 0xF4, 0xF6, 0xF2, 0xFB, 0xF9,
  0xFF, 0xD6, 0xDC, 0xA2, 0xA3, 0xA5, 0x20A7, 0x192,
  0xE1, 0xED, 0xF3, 0xFA, 0xF1, 0xD1, 0xAA, 0xBA,
  0xBF, 0x2310, 0xAC, 0xBD, 0xBC, 0xA1, 0xAB, 0xBB,
  0x2591, 0x2592, 0x2593, 0x2502, 0x2524, 0x2561, 0x2562, 0x2556,
  0x2555, 0x2563, 0x2551, 0x2557, 0x255D, 0x255C, 0x255B, 0x2510,
  0x2514, 0x2534, 0x252C, 0x251C, 0x2500, 0x253C, 0x255E, 0x255F,
  0x255A, 0x2554, 0x2569, 0x2566, 0x2560, 0x2550, 0x256C, 0x2567,
  0x2568, 0x2564, 0x2565, 0x2559, 0x2558, 0x2552, 0x2553, 0x256B,
  0x256A, 0x2518, 0x250C, 0x2588, 0x2584, 0x258C, 0x2590, 0x2580,
  0x3B1, 0xDF, 0x393, 0x3C0, 0x3A3, 0x3C3, 0xB5, 0x3C4,
  0x3A6, 0x398, 0x3A9, 0x3B4, 0x221E, 0x3C6, 0x3B5, 0x2229,
  0x2261, 0xB1, 0x2265, 0x2264, 0x2320, 0x2321, 0xF7,
  0x2248, 0xB0, 0x2219, 0xB7, 0x221A, 0x207F, 0xB2, 0x25A0, 0xA0
]);

const charmap_low = new Uint16Array([
  0x20, 0x263A, 0x263B, 0x2665, 0x2666, 0x2663, 0x2660, 0x2022,
  0x25D8, 0x25CB, 0x25D9, 0x2642, 0x2640, 0x266A, 0x266B, 0x263C,
  0x25BA, 0x25C4, 0x2195, 0x203C, 0xB6, 0xA7, 0x25AC, 0x21A8,
  0x2191, 0x2193, 0x2192, 0x2190, 0x221F, 0x2194, 0x25B2, 0x25BC
]);

var charmap = [],
  chr;

for (var i = 0; i < 256; i++) {
  if (i > 127) {
    chr = charmap_high[i - 0x80];
    charmap[i] = String.fromCharCode(chr);
  } else if (i < 32) {
    chr = charmap_low[i];
    charmap[i] = String.fromCharCode(chr);
  } else {
    chr = i;
    charmap[i] = String.fromCharCode(chr);
  }
}


let e;
// TODO: take GRAPHIC_FPS from env
var GRAPHIC_FPS = 5;
var GRAPHIC_FRAME_RATE = 1000 / GRAPHIC_FPS;
const HOST = process.env.host || '127.0.0.1';
const PORT = parseInt(process.env.port || 5348);
const client = require('net').createConnection({
  host: HOST,
  port: PORT
}, init);
var is_graphical = false;
var graphic_screen;
var graphic_context;
var
  graphic_image_data,
  graphic_buffer,
  graphic_buffer32,
  graphical_mode_width,
  graphical_mode_height;
var
  text_mode_sx = 9,
  text_mode_sy = 16,
  text_mode_width = 80,
  text_mode_height = 25,
  text_screen_width = text_mode_width * text_mode_sx,
  text_screen_height = text_mode_height * text_mode_sy;
var
  changed_rows = new Int8Array(text_mode_width),
  text_mode_data = new Int32Array(text_mode_width * text_mode_height * 3);
const sens = 0.2;
var m_downs = [false, false, false];

function resize_canvas(new_width, new_height) {
  graphic_screen = createCanvas(new_width, new_height);
  graphic_context = graphic_screen.getContext('2d');
  graphic_context["imageSmoothingEnabled"] = false;
}

client.on('data', async function(e) {
  try {
    const buf = JSON.parse('[' + e.toString().replaceAll('}{', '},{') + ']');
    for (var i = 0; i < buf.length; i++) {
      await process_data(buf[i]);
    }
    // process_data(JSON.parse(e.toString()));
  } catch (e) {
	  //console.log(e);
  }
});

client.on('end', function() {
  console.log('Disconnected from server');
});

client.on('error', function(err) {
  //console.log(err);
});

function send_msg(message) {
  const all_msg = JSON.stringify(message);
  client.write((all_msg.length + '          ').slice(0, 10) + all_msg);
}

function reset_timer() {
  clearInterval(update_text);
  clearInterval(update_graphical);
  setInterval(is_graphical ? update_text : update_graphical, GRAPHIC_FRAME_RATE);
}

var skip_space = true;

const hex_to_rgb = hex =>
  hex.replace(/^#?([a-f\d])([a-f\d])([a-f\d])$/i, (m, r, g, b) => '#' + r + r + g + g + b + b)
  .substring(1).match(/.{2}/g)
  .map(x => parseInt(x, 16));


function number_as_color(n) {
  n = n.toString(16);
  return hex_to_rgb('#' + Array(7 - n.length).join("0") + n);
}

function init() {
  console.log('Connected at ' + HOST + ':' + PORT + '.');
  resize_canvas(720, 400);
  // TODO: take wasm_path, bios, vga_bios from process.env
  e = new v86.V86Starter({
    wasm_path: "./build/v86.wasm",
    memory_size: 64 * 1024 * 1024,
    vga_memory_size: 4 * 1024 * 1024,
    bios: {
      url: "./bios/seabios.bin",
    },
    vga_bios: {
      url: "./bios/vgabios.bin",
    },
    hda: {
      url: "test_images/windows1.img"
      //url: "test_images/31.img"
      //url: "test_images/copy_winnt.img"
    },
    cdrom: {
      //url: "test_images/kolibri.iso"
    },
    autostart: true,
  });
  e.bus.register("screen-set-mode", function(data) {
    is_graphical = data;
    reset_timer();
    send_msg({m: data});
  });
  e.bus.register("screen-clear", function() {
    send_msg({c: true});
  });
  e.bus.register("screen-set-size-graphical", function(data) {
    graphical_mode_width = data[0];
    graphical_mode_height = data[1];
    resize_canvas(data[0], data[1]);
    graphic_image_data = graphic_context.createImageData(data[2], data[3]);
    graphic_buffer = new Uint8Array(graphic_image_data.data.buffer);
    graphic_buffer32 = new Int32Array(graphic_image_data.data.buffer);
    e.bus.send("screen-tell-buffer", [graphic_buffer32], [graphic_buffer32.buffer]);
    send_msg({sg: [data[0], data[1]]});
  });
  e.bus.register("screen-set-size-text", function(data) {
    if (data[0] === text_mode_width && data[1] === text_mode_height) {
      return;
    }
    text_mode_width = data[0];
    text_mode_height = data[1];
    changed_rows = new Int8Array(data[0]);
    text_mode_data = new Int32Array(data[0] * data[1] * 3);
    send_msg({st: data});
  });
  e.bus.register("screen-update-cursor", function(data) {
    // TODO: finish function
    send_msg({n: data});
  });
  e.bus.register("screen-update-cursor-scanline", function(data) {
    // TODO: finish function
    if (data[0] & 0x20) {
      send_msg({hc: true});
    } else {
      send_msg({sc: [Math.min(15, data[1] - data[0]), Math.min(15, data[0])]});
    }
  });
  e.bus.register("screen-fill-buffer-end", function(data) {
    data.forEach((layer) => {
      graphic_context.putImageData(
        graphic_image_data,
        layer.screen_x - layer.buffer_x,
        layer.screen_y - layer.buffer_y,
        layer.buffer_x,
        layer.buffer_y,
        layer.buffer_width,
        layer.buffer_height
      );
    });
    send_msg({g: graphic_screen.toDataURL().substr(22)});
  });
  e.bus.register("screen-put-char", function(data) {
    var chr = charmap[data[2]];
    if (!chr || !chr.replace(/[^\x00-\x7F]/g, ""))
      return;
    if (skip_space) {
      if (chr == ' ')
        return;
      //skip_space = false;
    }
    send_msg({v: [
        data[0],
        data[1],
        chr,
        number_as_color(data[3]),
        number_as_color(data[4])
    ]});
  });
  send_msg({init: true});
  reset_timer();
}

function update_text() {
  send_msg({});
}

function update_graphical() {
  e.bus.send('screen-fill-buffer');
}

function send_to_controller(code) {
  e.bus.send("keyboard-code", code);
}

async function process_data(msg) {
  if (msg.x || msg.y) {
    e.bus.send(
      "mouse-delta", [
        msg.x ? (msg.x * sens) : 0,
        msg.y ? (msg.y * -sens) : 0
      ]
    );
  }
  if (msg.d) {
    e.bus.send("mouse-click", msg.d);
  }
  if (msg.a) {
    for (var i = 0; i < msg.a.length; i++) {
      if (msg.a[i] > 0xFF) {
        send_to_controller(msg.a[i] >> 8);
        send_to_controller(msg.a[i] & 0xFF);
      } else {
        send_to_controller(msg.a[i]);
      }
    }
  }
  if (msg.b) {
    for (var i = 0; i < msg.b.length; i++) {
      msg.b[i] |= 0x80;
      if (msg.b[i] > 0xFF) {
        send_to_controller(msg.b[i] >> 8);
        send_to_controller(msg.b[i] & 0xFF);
      } else {
        send_to_controller(msg.b[i]);
      }
    }
  }
  if (msg.q) {
    client.destroy();
  }
  //send_msg({'n': true});
}
