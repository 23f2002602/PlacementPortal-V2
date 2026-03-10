<template>
<div class="page">

<div class="card">

<h2>Student Registration</h2>

<input v-model="name" placeholder="Name" />
<input v-model="email" placeholder="Email" />
<input v-model="password" type="password" placeholder="Password" />
<input v-model="roll_number" placeholder="Roll Number" />
<input v-model="branch" placeholder="Branch" />

<button @click="register">Register</button>

</div>

</div>
</template>

<script>
import API from "@/utils/api"

export default{

 data(){
  return{
   name:"",
   email:"",
   password:"",
   roll_number:"",
   branch:""
  }
 },

 methods:{

 async register(){

   await API.post("/auth/register",{

     name:this.name,
     email:this.email,
     password:this.password,
     role:"student",
     roll_number:this.roll_number,
     branch:this.branch

   })

   alert("Registered Successfully")

 }

 }

}
</script>

<style>
.page{
height:100vh;
background:#020617;
display:flex;
justify-content:center;
align-items:center;
}

.card{
background:#0f172a;
padding:40px;
border-radius:10px;
display:flex;
flex-direction:column;
gap:10px;
width:350px;
color:white;
}

.card input{
padding:10px;
border-radius:6px;
border:none;
}

.card button{
padding:10px;
background:#2563eb;
border:none;
border-radius:6px;
color:white;
}

</style>