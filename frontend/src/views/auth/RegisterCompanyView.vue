<template>
<div class="page">

<div class="card">

<h2>Company Registration</h2>

<input v-model="name" placeholder="HR Name" />
<input v-model="email" placeholder="Email" />
<input v-model="password" type="password" placeholder="Password" />
<input v-model="company_name" placeholder="Company Name" />
<input v-model="industry" placeholder="Industry" />

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
 company_name:"",
 industry:""

 }

 },

 methods:{

 async register(){

 await API.post("/auth/register",{

 name:this.name,
 email:this.email,
 password:this.password,
 role:"company",
 company_name:this.company_name,
 industry:this.industry

 })

 alert("Company Registered. Await admin approval")

 }

 }

}
</script>