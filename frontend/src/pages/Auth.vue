<template>
	<div class="flex h-screen overflow-hidden sm:bg-gray-50">
		<div class="w-full overflow-auto">
			<div class="relative h-full">
				<div class="relative z-10 mx-auto py-8 sm:w-max sm:py-32">
					<div class="flex flex-row items-center justify-center gap-2">
						<div class="w-7 h-7 inline">
							<svg
								fill="none"
								viewBox="0 0 25 25"
								xmlns="http://www.w3.org/2000/svg"
							>
								<g clip-path="url(#clip0_8154_27281)">
									<path
										d="M19.9624 0.763672H5.83963C3.31294 0.763672 1.26465 2.81189 1.26465 5.33849V19.4608C1.26465 21.9874 3.31294 24.0356 5.83963 24.0356H19.9624C22.4891 24.0356 24.5374 21.9874 24.5374 19.4608V5.33849C24.5374 2.81189 22.4891 0.763672 19.9624 0.763672Z"
										fill="#383838"
									></path>
									<path
										d="M9.17773 7.97852H16.625"
										stroke="white"
										stroke-width="2.10048"
									></path>
									<path
										d="M10.2246 17.8705V12.9834H16.0428"
										stroke="white"
										stroke-width="2.10048"
									></path>
								</g>
								<defs>
									<clipPath id="clip0_8154_27281">
										<rect
											fill="white"
											height="23.9992"
											transform="translate(0.901367 0.400391)"
											width="24"
										></rect>
									</clipPath>
								</defs>
							</svg>
						</div>
						<span
							class="select-none text-xl font-semibold tracking-tight text-gray-900"
						>
							Frappe Build CTF
						</span>
					</div>

					<div
						class="mx-auto w-full bg-white px-4 py-8 sm:mt-6 sm:w-96 sm:rounded-lg sm:px-8 sm:shadow-xl"
					>
						<div>
							<div class="flex flex-col gap-3">
								<FormControl
									label="Email"
									variant="outline"
									type="email"
									placeholder="johndoe@mail.com"
									autocomplete="email"
									v-model="email"
									required
								/>
								<div class="flex flex-row gap-4" v-if="auth_info.is_signup">
									<FormControl
										label="First Name"
										type="text"
										variant="outline"
										placeholder="John"
										v-model="auth_info.first_name"
										:disabled="auth_info.is_verification_code_sent"
										required
									/>
									<FormControl
										label="Last Name"
										type="text"
										variant="outline"
										placeholder="Doe"
										v-model="auth_info.last_name"
										:disabled="auth_info.is_verification_code_sent"
										required
									/>
								</div>
								<FormControl
									v-if="auth_info.is_verification_code_sent"
									label="Verification code"
									type="text"
									variant="outline"
									placeholder="123456"
									maxlength="6"
									v-model="auth_info.verification_code"
									required
								/>
								<ErrorMessage
									:message="
										loginResource.error ||
										registerResource.error ||
										verifyCodeResource.error
									"
								/>
								<Button
									variant="solid"
									v-if="!auth_info.is_verification_code_sent"
									:loading="loginResource.loading || registerResource.loading"
									@click="proceedToNextStep()"
									class="mt-4"
								>
									Proceed to Next Step
								</Button>
								<Button
									class="mt-4"
									variant="solid"
									v-if="auth_info.is_verification_code_sent"
									:loading="verifyCodeResource.loading"
									loadingText="Verifying..."
									@click="verifyCodeResource.submit()"
								>
									Verify Code
								</Button>
								<Button
									variant="outline"
									v-if="auth_info.is_verification_code_sent"
									@click="resendVerificationCode()"
									:loading="
										resendVerificationCodeARResource.loading ||
										loginResource.loading
									"
								>
									Didn't receive verification code? Resend
								</Button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { FormControl, Button, ErrorMessage, createResource } from 'frappe-ui'
import { reactive, ref, watch } from 'vue'
import { toast } from 'vue-sonner'

const email = ref('')
const auth_info = reactive({
	is_signup: false,
	is_verification_code_sent: false,
	first_name: '',
	last_name: '',
	account_request: '',
	verification_code: '',
})

watch(email, () => {
	auth_info.first_name = ''
	auth_info.last_name = ''
	auth_info.is_signup = false
	auth_info.is_verification_code_sent = false
	auth_info.verification_code = ''
})

const loginResource = createResource({
	url: '/api/method/ctf.api.auth.login',
	auto: false,
	method: 'POST',
	makeParams: () => ({
		email: email.value,
	}),
	onSuccess: (data) => {
		auth_info.is_signup = data.account_exists == false
		if (!auth_info.is_signup) {
			auth_info.is_verification_code_sent = true
		}
		if (auth_info.is_signup) {
			toast.message('Please provide your name to continue')
		}
	},
})

const registerResource = createResource({
	url: '/api/method/ctf.api.auth.register',
	auto: false,
	method: 'POST',
	makeParams: () => ({
		email: email,
		first_name: auth_info.first_name,
		last_name: auth_info.last_name,
	}),
	onSuccess: (ar) => {
		auth_info.account_request = ar
		auth_info.is_verification_code_sent = true
	},
})

const verifyCodeResource = createResource({
	url: '/api/method/ctf.api.auth.verify_code',
	auto: false,
	method: 'POST',
	makeParams: () => ({
		code: auth_info.verification_code,
		email: auth_info.is_signup ? null : email,
		ar: auth_info.is_signup ? auth_info.account_request : null,
	}),
	onSuccess: () => {
		window.location.href = '/'
	},
})

const resendVerificationCodeARResource = createResource({
	url: '/api/method/ctf.api.auth.resend_verification_code',
	auto: false,
	method: 'POST',
	makeParams: () => ({
		ar: auth_info.account_request,
	}),
})

const proceedToNextStep = () => {
	if (auth_info.is_signup) {
		registerResource.submit()
	} else {
		loginResource.submit()
	}
}

const resendVerificationCode = () => {
	if (auth_info.is_signup) {
		resendVerificationCodeARResource.submit()
	} else {
		loginResource.submit()
	}
	toast.success('Requested to resend verification code')
	auth_info.verification_code = ''
	verifyCodeResource.reset()
}
</script>
