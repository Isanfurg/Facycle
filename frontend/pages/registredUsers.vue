<template>
    <v-row class="custom-content ma-0 pa-0" align="top" justify="center">
        <v-col class="px-12" cols="12">
           <v-card
                class="mx-auto"
                color="#EC994B"
                style="padding: 5px"
                min-width="20%"
                max-widht="40%"
            >
                <v-list max-widht="40%" color="#73777B">
                    <v-subheader min-widht="40%" max-widht="40%" class="textWhite"> <h1>Usuarios Registrados</h1> </v-subheader>
                    <hr />
                    <v-list-item v-for="user in users" :key="user.email">
                      <v-list-item-avatar>
                        <v-img src="https://simulacionymedicina.es/wp-content/uploads/2015/11/default-avatar-300x300-1.jpg" ></v-img>
                     </v-list-item-avatar>
                      <v-list-item-content>
                        <v-list-item-title>{{user.email}}</v-list-item-title>
                        <v-list-item-subtitle>{{user.user_name}}</v-list-item-subtitle>
                      </v-list-item-content>
                  
               

                    </v-list-item>
                </v-list>
            </v-card>
        </v-col>
    </v-row>
</template>
<script>
import axios from "axios";
export default {
	name: "registredUsers",
	components: {
	    },
	data() {
	  return {
      users: [],
	  }
	},
  methods: {
    
  },
  created() {
    axios.get('http://127.0.0.1:5000/api/getUsers')
    .then(response => {
      // JSON responses are automatically parsed.
      this.users = response.data
      console.log(this.users)
    })
    .catch(e => {
      this.errors.push(e)
    })
  },
  
}
</script>
<style scoped>
.custom-content {
  background-color: #F1EEE9;
  margin: 0 0 0 0;
  height: 100%;
}
hr {
  font-size: 54px;
  width: 100%;
  border-color: #EC994B;
}
.textBlack{
  color: #000;
}
.textWhite{
  color: #fff;
}
.textPrimary{
  color: #EC994B;
}
</style>
