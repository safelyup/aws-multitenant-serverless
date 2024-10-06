<template>
<Authenticator :form-fields="formFields">
<template v-slot:header>
  <div style="padding: var(--amplify-space-large); text-align: center">
    <img
      class="amplify-image"
      alt="Amplify logo"
      src="https://docs.amplify.aws/assets/logo-dark.svg"
    />
  </div>
</template>
<template v-slot:footer>
  <div style="padding: var(--amplify-space-large); text-align: center">
    <p class="amplify-text" style="color: var(--amplify-colors-neutral-80)">
      &copy; example
    </p>
  </div>
</template>
<NuxtLayout>
  <NuxtPage />
</NuxtLayout>
</Authenticator>
</template>

<script setup>
import { Authenticator } from "@aws-amplify/ui-vue";
import "@aws-amplify/ui-vue/styles.css";
import { Amplify } from 'aws-amplify';
Amplify.configure({
  Auth: {
    region: 'us-east-1',
    userPoolId: '<POOL ID>',
    userPoolWebClientId: '<POOL WEBCLIENT ID>',
    oauth: {
      domain: 'https://example-demo.auth.us-east-1.amazoncognito.com',
      scope: [
        'email',
        'profile',
        'openid'
      ],
      redirectSignIn: 'http://localhost:3000/',
      redirectSignOut: 'http://localhost:3000/',
      clientId: '<POOL WEBCLIENT ID>',
      responseType: 'code'
    }
  }
});
const formFields = {
  signIn: {
    username: {
      placeholder: 'Enter Your Email',
      isRequired: true,
      label: 'Email'
    },
  },
  setupTOTP: {
    QR: {
      totpIssuer: 'example',
      totpUsername: "orgName",
    },
  }
}
</script>
<style>
body {
  background-color: white;
}
.amplify-tabs {
  display: none;
}
:root, [data-amplify-theme] {
--amplify-colors-brand-primary-10: #cffafe;
--amplify-colors-brand-primary-20: #a5f3fc;
--amplify-colors-brand-primary-40: #67e8f9;
--amplify-colors-brand-primary-60: #22d3ee;
--amplify-colors-brand-primary-80: #0891b2;
--amplify-colors-brand-primary-90: #0e7490;
--amplify-colors-brand-primary-100: #155e75;
--amplify-colors-border-primary: var(--amplify-colors-neutral-40);
--amplify-colors-border-secondary: var(--amplify-colors-neutral-20);
--amplify-border-widths-small: 1px;
--amplify-border-widths-medium: 2px;
--amplify-border-widths-large: 4px;
}
</style>
