<template>
  <v-app-bar color="primary">
    <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn variant="outlined" v-bind="props">マニュアル</v-btn>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title>
            <a href="https://drive.google.com/file/d/1xaJvoquj3cUJIc7RjSeD4cv1Cur5XV1C/view?usp=sharing" target="_blank">学生向け</a>
          </v-list-item-title>
        </v-list-item>
        <v-list-item>
          <v-list-item-title>
            <a href="https://drive.google.com/file/d/1hr9HqzCcTzFmYxK6YVz3fCgiWTjlqd80/view?usp=sharing" target="_blank">教員向け</a>
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>