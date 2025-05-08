/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import '@mdi/js'
import 'vuetify/styles'

// Composables
import { createVuetify, ThemeDefinition } from 'vuetify'


export const randomColor = () => {
  return "#" + [0, 1, 2, 3, 4, 5]
    .map(_ => Math.floor(Math.random() * 0x10).toString(16))
    .join("");
}

const primarycolor = randomColor()
const secondarycolor = randomColor()



const theme1: ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#3b96c3',
    secondary: '#e7881a',
  }
}

const theme2: ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#7bc1bb',
    secondary: '#d07986',
  }
}

const theme3: ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#A066dd',
    secondary: '#99D0F0',
  }
}

const theme4: ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#cf2b0e',
    secondary: '#162e3a',
  }
}

const theme5: ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#232122',
    secondary: '#7ba4a8',
  }
}
const theme6: ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#2C6B6A',
    secondary: '#C39140',
  }
}
const theme7:ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#f18d9e',
    secondary: '#5bc8ac',
  }
}
const theme8:ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#FAA755',
    secondary: '#DAC4A5',
  }
}
const theme9: ThemeDefinition = {
  dark: false,
  colors: {
    primary: '#1C6BC2',
    secondary: '#48A9A6',
  }
}
const theme10: ThemeDefinition = {
  dark: false,
  colors: {
    primary: primarycolor,
    secondary: secondarycolor,
  }
}

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides


const savedTheme = 'light';

//const savedTheme = localStorage.getItem('selectedTheme') ||'light';

export default createVuetify({
  theme: {
    defaultTheme: savedTheme,
    themes: {
      theme1,
      theme2,
      theme3,
      theme4,
      theme5,
      theme6,
      theme7,
      theme8,
      theme9,
      theme10
    }
  }
})