<template>
  <div class="container">
    <form class="login-form">
      <div class="form-group mb-3">
        <label for="exampleInputEmail1">Email address</label>
        <input
          v-model="login"
          type="email"
          class="form-control"
          id="exampleInputEmail1"
          aria-describedby="emailHelp"
          placeholder="Enter email"
        />
        <small id="emailHelp" class="form-text text-muted"
          >We'll never share your email with anyone else.</small
        >
      </div>
      <div class="form-group mb-4">
        <label for="exampleInputPassword1">Password</label>
        <input
          v-model="password"
          type="password"
          class="form-control"
          id="exampleInputPassword1"
          placeholder="Password"
        />
      </div>
      <button type="submit" class="btn btn-primary" v-on:click.prevent="logIn">
        Submit
      </button>
    </form>
  </div>
</template>

<script src="./component.js"></script>
