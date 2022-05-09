<template witdh="100%" height="100" class="ma-0 pa-0">
  <v-app>
    <v-toolbar dense fluid height="60px" max-height="60px" color="#73777B" class="ma-0 pa-0">
      
     <router-link to="/" class="ma-0 pa-0">
       <v-img contain min-height="50px" max-height="50px"  max-width="100px" src="logo.png" class="ma-0 pa-0"></v-img> 
     </router-link>
      <router-link v-for="link in links" :key="link.tittle" :to="link.ref" class="hidden-sm-and-down">
        <v-btn
          large
          plain
          class="text-center white--text"
          color="#02B5C2"
        >
          {{ link.tittle }}
        </v-btn>
      </router-link>
      <v-spacer/>

    </v-toolbar>
    
    <Nuxt />
    <v-card fluid absolute width="100%" min-height="60px" max-height="150px" color="#73777B" elevation="4" class="ma-0 pa-0 pt-4">
      <v-card-text class="ma-0 pa-0 px-5">
        <v-row class="ma-0 pa-0">
          <v-col sm="12" md="3" class="ma-0 pa-0">
            <v-btn
              v-for="icon in icons"
              :key="icon"
              class="mx-1"
              icon
              style="color: white"
            >
              <v-icon size="24px">
                {{ icon }}
              </v-icon>
            </v-btn>
          </v-col>
          <v-col
            sm="12"
            md="6"
            justify="center"
            style="color: white"
            class="text-center ma-0 pa-0"
          >
            Facycle®2022
          </v-col>
          <v-col
            sm="12"
            md="3"

            justify="right"
            style="color: white"
            class="text-right ma-0 pa-0"
          >
            TTC
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-app>
</template>


<script>
export default {
  name: 'DefaultLayout',
  data () {
    return {
      icons: [
        'mdi-chart-bubble',
        'mdi-facebook',
        'mdi-twitter',
        'mdi-linkedin',
        'mdi-instagram',
      ],
      links: [

        {
          tittle: 'Registrar',
          ref: '/',
        },
        {
          tittle: 'Abrir Candado',
          ref: '/sensor',

        },
      ],
    }
  }
}
</script>
