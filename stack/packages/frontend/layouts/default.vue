<template>
  <UContainer>
    <div class="lg:col-span-10 min-h-0 flex flex-col">
      <div class="pt-2 pb-16 lg:col-span-8">
        <UCard>
          <template #header>
            <h1 class="text-2xl font-bold tracking-tight">My Dashboard</h1>
          </template>
          Email: {{ user.attributes.email }}<br />
          Role: {{ user.attributes['custom:userRole'] }}<br />
          OrgID: {{ user.attributes['custom:orgId'] }}<br />
          IdToken: <pre style="overflow: hidden;">{{ user.signInUserSession.idToken.jwtToken }}</pre><br />
          <UButton label="SignOut" @click="auth.signOut()" />
        </UCard>
        
        <slot />
      </div>
    </div>
  </UContainer>
</template>

<script setup>
import { useAuthenticator } from "@aws-amplify/ui-vue";
const auth = useAuthenticator()
const user = auth.user
useHead({
  bodyAttrs: {
    class: "antialiased font-sans text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-800"
  },
});
</script>
