<template>

<span :class="badgeClass">

{{status}}

</span>

</template>


<script>

export default{

props:["status"],

computed:{

badgeClass(){

if(this.status==="approved") return "green"
if(this.status==="rejected") return "red"

return "yellow"

}

}

}

</script>


<style>

.green{color:green}
.red{color:red}
.yellow{color:orange}

</style>