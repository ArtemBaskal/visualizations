const frequencyComponents = [
  {
    low: 941,
    high: 1336,
  },
  {
    low: 697,
    high: 1209,
  },
  {
    low: 697,
    high: 1336,
  },
  {
    low: 697,
    high: 1477,
  },
  {
    low: 770,
    high: 1209,
  },
  {
    low: 770,
    high: 1336,
  },
  {
    low: 770,
    high: 1477,
  },
  {
    low: 852,
    high: 1209,
  },
  {
    low: 852,
    high: 1336,
  },
  {
    low: 852,
    high: 1477,
  }];

const WIDTH = 1260;
const HALF_SECOND = 0.5;
const drawGraph = (tone = 0) => {
  if (document.getElementById(tone)) {
    return;
  }
  document.body.innerHTML = '';
  const canvas = document.createElement('canvas');
  const h1 = document.createElement('h1');
  h1.innerText = `DTMF ${tone}`;
  h1.style = 'font-family: Montserrat,sans-serif; font-weight: 200';
  canvas.setAttribute('id', tone);
  canvas.setAttribute('width', WIDTH.toString());
  canvas.setAttribute('height', '400');
  document.body.appendChild(h1);
  document.body.appendChild(canvas);

  const c = document.getElementById(tone);
  const ctx = c.getContext('2d');
  ctx.stroke();
  let angularFrequency1 = 0;
  let angularFrequency2 = 0;
  let x = 0;
  let y = 180;
  for (let i = 0;
    i < WIDTH;
    i += 10) {
    ctx.moveTo(i + 5, 180);
    ctx.lineTo(i, 180);
  }
  ctx.stroke();
  const amplitude = 80;
  const frequency1 = (Math.PI / frequencyComponents[tone].high) * 10;
  const frequency2 = (Math.PI / frequencyComponents[tone].low) * 10;
  for (let t = 0; t <= WIDTH; t += 1) {
    ctx.moveTo(x, y);
    x = t;
    const sin1 = Math.sin(angularFrequency1);
    const sin2 = Math.sin(angularFrequency2);
    y = Math.floor(180 - amplitude * (sin1 + sin2));
    angularFrequency1 += frequency1;
    angularFrequency2 += frequency2;
    ctx.lineTo(x, y);
    ctx.stroke();
  }
};
window.AudioContext = window.AudioContext || window.webkitAudioContext;
const playTone = (tone, options) => {
  console.log('тон', tone);
  if (tone === null) {
    return;
  }
  // eslint-disable-next-line no-shadow
  const { sampleRate, volume } = options;
  try {
    const audioCtx = new AudioContext({ sampleRate });
    const oscillator1 = audioCtx.createOscillator();
    const oscillator2 = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    gainNode.gain.value = volume;
    gainNode.gain.setValueAtTime(0, audioCtx.currentTime + HALF_SECOND);
    oscillator1.connect(gainNode);
    oscillator2.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    oscillator1.frequency.value = frequencyComponents[tone].low;
    oscillator2.frequency.value = frequencyComponents[tone].high;
    oscillator1.start(0);
    oscillator2.start(0);
    oscillator1.stop(HALF_SECOND);
    oscillator2.stop(HALF_SECOND);
  } catch (err) {
    console.error(err);
  }
};

function delay() {
  return new Promise((resolve) => setTimeout(resolve, HALF_SECOND * 1000));
}

async function delayedPlay(tone, options, isGraphNeeded) {
  playTone(tone, options);
  if (isGraphNeeded) {
    drawGraph(tone);
  } else if (document.querySelectorAll('canvas').length) {
    document.body.innerHTML = '';
  }
  await delay();
}

// eslint-disable-next-line no-shadow
const inputTone = async (
  tones = prompt('Введите тон'),
  sampleRate = 10000,
  volume = HALF_SECOND) => {
  const options = {
    sampleRate,
    volume,
  };
  if (tones === null || tones === '') {
    return;
  }
  let isGraphNeeded = true;
  const formattedTones = tones.toString()
    .match(/\d/g);
  if (formattedTones.length > 1) {
    isGraphNeeded = true;
    console.log('тона:', formattedTones.join(','));
  }
  // eslint-disable-next-line no-restricted-syntax
  for (const tone of formattedTones) {
    // eslint-disable-next-line no-await-in-loop
    await delayedPlay(tone, options, isGraphNeeded);
  }
  inputTone();
};

const f = () => {
  const h1 = document.createElement('h1');
  h1.innerText = 'DTMF';
  document.body.appendChild(h1);
  h1.addEventListener('click', () => inputTone());
};

f();
