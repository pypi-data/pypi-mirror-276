<script lang="ts">
	import {
		beforeUpdate,
		afterUpdate,
		createEventDispatcher,
		tick,
	} from "svelte";
	import { BlockTitle } from "@gradio/atoms";
	import type { SelectData } from "@gradio/utils";
	import { fadeSlide } from "./transitions.js";

	export let value = "";
	export let value_is_output = false;
	export let lines = 1;
	export let placeholder = "Type here...";
	export let label: string;
	export let info: string | undefined = undefined;
	export let disabled = false;
	export let show_label = true;
	export let container = true;
	export let max_lines: number;
	export let prompts: string[] = [];
	export let suffixes: string[] = [];
	export let rtl = false;
	export let autofocus = false;
	export let text_align: "left" | "right" | undefined = undefined;
	export let autoscroll = true;

	let el: HTMLTextAreaElement | HTMLInputElement;
	let show_menu = false;
	let can_scroll: boolean;
	let previous_scroll_top = 0;
	let user_has_scrolled_up = false;
	let ongoing_animation = false;

	let show_magic =
		!ongoing_animation && (prompts.length > 0 || suffixes.length > 0);

	$: value, el && lines !== max_lines && resize({ target: el });

	$: if (value === null) value = "";

	const dispatch = createEventDispatcher<{
		change: string;
		submit: undefined;
		blur: undefined;
		select: SelectData;
		input: undefined;
		focus: undefined;
	}>();

	beforeUpdate(() => {
		can_scroll =
			el && el.offsetHeight + el.scrollTop > el.scrollHeight - 100;
	});

	const scroll = (): void => {
		if (can_scroll && autoscroll && !user_has_scrolled_up) {
			el.scrollTo(0, el.scrollHeight);
		}
	};

	function handle_change(): void {
		dispatch("change", value);
		if (!value_is_output) {
			dispatch("input");
		}
	}
	afterUpdate(() => {
		if (autofocus) {
			el.focus();
		}
		if (can_scroll && autoscroll) {
			scroll();
		}
		value_is_output = false;
		show_magic =
			!ongoing_animation && (prompts.length > 0 || suffixes.length > 0);
	});
	$: value, handle_change();

	async function handle_extension(): Promise<void> {
		show_menu = !show_menu;
	}

	function addSuffix(word) {
		// Add a comma and space if the value is not empty
		if (value.trim()) {
			value += ", ";
		}
		value += `${word}`;
	}

	function loadPrompt(word) {
		value += `${word}`;
	}

	function handle_select(event: Event): void {
		const target: HTMLTextAreaElement | HTMLInputElement = event.target as
			| HTMLTextAreaElement
			| HTMLInputElement;
		const text = target.value;
		const index: [number, number] = [
			target.selectionStart as number,
			target.selectionEnd as number,
		];
		dispatch("select", { value: text.substring(...index), index: index });
	}

	async function handle_keypress(e: KeyboardEvent): Promise<void> {
		await tick();
		if (e.key === "Enter" && e.shiftKey && lines > 1) {
			e.preventDefault();
			dispatch("submit");
		} else if (
			e.key === "Enter" &&
			!e.shiftKey &&
			lines === 1 &&
			max_lines >= 1
		) {
			e.preventDefault();
			dispatch("submit");
		}
	}

	function handle_scroll(event: Event): void {
		const target = event.target as HTMLElement;
		const current_scroll_top = target.scrollTop;
		if (current_scroll_top < previous_scroll_top) {
			user_has_scrolled_up = true;
		}
		previous_scroll_top = current_scroll_top;

		const max_scroll_top = target.scrollHeight - target.clientHeight;
		const user_has_scrolled_to_bottom =
			current_scroll_top >= max_scroll_top;
		if (user_has_scrolled_to_bottom) {
			user_has_scrolled_up = false;
		}
	}

	async function resize(
		event: Event | { target: HTMLTextAreaElement | HTMLInputElement },
	): Promise<void> {
		await tick();
		if (lines === max_lines) return;

		let max =
			max_lines === undefined
				? false
				: max_lines === undefined // default
					? 21 * 11
					: 21 * (max_lines + 1);
		let min = 21 * (lines + 1);

		const target = event.target as HTMLTextAreaElement;
		target.style.height = "1px";

		let scroll_height;
		if (max && target.scrollHeight > max) {
			scroll_height = max;
		} else if (target.scrollHeight < min) {
			scroll_height = min;
		} else {
			scroll_height = target.scrollHeight;
		}

		target.style.height = `${scroll_height}px`;
	}

	function text_area_resize(
		_el: HTMLTextAreaElement,
		_value: string,
	): any | undefined {
		if (lines === max_lines) return;
		_el.style.overflowY = "scroll";
		_el.addEventListener("input", resize);

		if (!_value.trim()) return;
		resize({ target: _el });

		return {
			destroy: () => _el.removeEventListener("input", resize),
		};
	}
</script>

<!-- svelte-ignore a11y-autofocus -->
<label class:container>
	<BlockTitle {show_label} {info}>{label}</BlockTitle>
	<div class="input-container">
		{#if !ongoing_animation && show_menu && show_magic}
			<div class="magic_container">
				<textarea
					data-testid="textbox"
					use:text_area_resize={value}
					class="scroll-hide"
					dir={rtl ? "rtl" : "ltr"}
					bind:value
					bind:this={el}
					{placeholder}
					rows={lines}
					{disabled}
					{autofocus}
					on:keypress={handle_keypress}
					on:blur
					on:select={handle_select}
					on:focus
					on:scroll={handle_scroll}
					style={text_align ? "text-align: " + text_align : ""}
				/>
				<button
					class="extend_button"
					on:click={handle_extension}
					aria-label="Extend"
					aria-roledescription="Extend text"
				>
					<svg
						width="26"
						height="26"
						viewBox="0 0 26 26"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M23.0978 15.6987L23.5777 15.2188L21.7538 13.3952L21.2739 13.8751L23.0978 15.6987ZM11.1253 2.74873L10.6454 3.22809L12.4035 4.98733L12.8834 4.50769L11.1253 2.74873ZM25.5996 9.23801H22.885V9.91673H25.5996V9.23801ZM10.6692 9.23801H7.95457V9.91673H10.6692V9.23801ZM21.8008 5.01533L23.5982 3.21773L23.118 2.73781L21.3206 4.53541L21.8008 5.01533ZM17.2391 7.29845L18.6858 8.74521C18.7489 8.80822 18.7989 8.88303 18.8331 8.96538C18.8672 9.04773 18.8847 9.13599 18.8847 9.22513C18.8847 9.31427 18.8672 9.40254 18.8331 9.48488C18.7989 9.56723 18.7489 9.64205 18.6858 9.70505L3.00501 25.3859C2.74013 25.6511 2.31061 25.6511 2.04517 25.3859L0.598406 23.9391C0.535351 23.8761 0.485329 23.8013 0.4512 23.719C0.417072 23.6366 0.399506 23.5483 0.399506 23.4592C0.399506 23.3701 0.417072 23.2818 0.4512 23.1995C0.485329 23.1171 0.535351 23.0423 0.598406 22.9793L16.2792 7.29845C16.3422 7.23533 16.417 7.18525 16.4994 7.15108C16.5817 7.11691 16.67 7.09932 16.7592 7.09932C16.8483 7.09932 16.9366 7.11691 17.019 7.15108C17.1013 7.18525 17.1761 7.23533 17.2391 7.29845ZM14.4231 13.2042L18.3792 9.24893L16.746 7.61541L12.7899 11.5713L14.4231 13.2042ZM17.4555 0.415771H16.7768V3.13037H17.4555V0.415771ZM17.4555 15.3462H16.7768V18.0608H17.4555V15.3462Z"
							fill="#ff6700"
						/>
					</svg>
				</button>
			</div>

			<div
				class="menu"
				in:fadeSlide={{ duration: 500 }}
				on:transitionstart={() => (ongoing_animation = true)}
				on:transitionend={() => (ongoing_animation = false)}
			>
				{#if prompts.length > 0}
					<div class="menu_section_prompt">
						<span> A few prompt inspirations </span>
						<ul>
							{#each prompts as word}
								<li>
									<button
										class="text_extension_button_prompt"
										on:click={() => loadPrompt(word)}
										><div>{word}</div>
										<div>
											<svg
												xmlns="http://www.w3.org/2000/svg"
												width="11"
												height="12"
												viewBox="0 0 11 12"
												fill="none"
											>
												<path
													d="M8.70801 5.51112H5.95801V2.57779C5.95801 2.44813 5.90972 2.32377 5.82376 2.23209C5.73781 2.14041 5.62123 2.0889 5.49967 2.0889C5.37812 2.0889 5.26154 2.14041 5.17558 2.23209C5.08963 2.32377 5.04134 2.44813 5.04134 2.57779V5.51112H2.29134C2.16978 5.51112 2.0532 5.56263 1.96725 5.65431C1.8813 5.746 1.83301 5.87035 1.83301 6.00001C1.83301 6.12967 1.8813 6.25402 1.96725 6.34571C2.0532 6.43739 2.16978 6.4889 2.29134 6.4889H5.04134V9.42223C5.04134 9.55189 5.08963 9.67624 5.17558 9.76793C5.26154 9.85961 5.37812 9.91112 5.49967 9.91112C5.62123 9.91112 5.73781 9.85961 5.82376 9.76793C5.90972 9.67624 5.95801 9.55189 5.95801 9.42223V6.4889H8.70801C8.82956 6.4889 8.94614 6.43739 9.0321 6.34571C9.11805 6.25402 9.16634 6.12967 9.16634 6.00001C9.16634 5.87035 9.11805 5.746 9.0321 5.65431C8.94614 5.56263 8.82956 5.51112 8.70801 5.51112Z"
													fill="#FF9A57"
												/>
											</svg>
										</div></button
									>
								</li>
							{/each}
						</ul>
					</div>
				{/if}
				{#if suffixes.length > 0}
					<div class="menu_section_style">
						<span> Add keywords to guide style </span>
						<ul>
							{#each suffixes as word}
								<li>
									<button
										class="text_extension_button"
										on:click={() => addSuffix(word)}
										><div>{word}</div>
										<div>
											<svg
												xmlns="http://www.w3.org/2000/svg"
												width="11"
												height="12"
												viewBox="0 0 11 12"
												fill="none"
											>
												<path
													d="M8.70801 5.51112H5.95801V2.57779C5.95801 2.44813 5.90972 2.32377 5.82376 2.23209C5.73781 2.14041 5.62123 2.0889 5.49967 2.0889C5.37812 2.0889 5.26154 2.14041 5.17558 2.23209C5.08963 2.32377 5.04134 2.44813 5.04134 2.57779V5.51112H2.29134C2.16978 5.51112 2.0532 5.56263 1.96725 5.65431C1.8813 5.746 1.83301 5.87035 1.83301 6.00001C1.83301 6.12967 1.8813 6.25402 1.96725 6.34571C2.0532 6.43739 2.16978 6.4889 2.29134 6.4889H5.04134V9.42223C5.04134 9.55189 5.08963 9.67624 5.17558 9.76793C5.26154 9.85961 5.37812 9.91112 5.49967 9.91112C5.62123 9.91112 5.73781 9.85961 5.82376 9.76793C5.90972 9.67624 5.95801 9.55189 5.95801 9.42223V6.4889H8.70801C8.82956 6.4889 8.94614 6.43739 9.0321 6.34571C9.11805 6.25402 9.16634 6.12967 9.16634 6.00001C9.16634 5.87035 9.11805 5.746 9.0321 5.65431C8.94614 5.56263 8.82956 5.51112 8.70801 5.51112Z"
													fill="#FF9A57"
												/>
											</svg>
										</div></button
									>
								</li>
							{/each}
						</ul>
					</div>
				{/if}
			</div>
		{:else if !ongoing_animation && !show_menu && show_magic}
			<div class="magic_container">
				<textarea
					data-testid="textbox"
					use:text_area_resize={value}
					class="scroll-hide"
					dir={rtl ? "rtl" : "ltr"}
					bind:value
					bind:this={el}
					{placeholder}
					rows={lines}
					{disabled}
					{autofocus}
					on:keypress={handle_keypress}
					on:blur
					on:select={handle_select}
					on:focus
					on:scroll={handle_scroll}
					style={text_align ? "text-align: " + text_align : ""}
				/>
				<button
					class="extend_button"
					on:click={handle_extension}
					aria-label="Extend"
					aria-roledescription="Extend text"
				>
					<svg
						width="26"
						height="26"
						viewBox="0 0 26 26"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M23.0978 15.6987L23.5777 15.2188L21.7538 13.3952L21.2739 13.8751L23.0978 15.6987ZM11.1253 2.74873L10.6454 3.22809L12.4035 4.98733L12.8834 4.50769L11.1253 2.74873ZM25.5996 9.23801H22.885V9.91673H25.5996V9.23801ZM10.6692 9.23801H7.95457V9.91673H10.6692V9.23801ZM21.8008 5.01533L23.5982 3.21773L23.118 2.73781L21.3206 4.53541L21.8008 5.01533ZM17.2391 7.29845L18.6858 8.74521C18.7489 8.80822 18.7989 8.88303 18.8331 8.96538C18.8672 9.04773 18.8847 9.13599 18.8847 9.22513C18.8847 9.31427 18.8672 9.40254 18.8331 9.48488C18.7989 9.56723 18.7489 9.64205 18.6858 9.70505L3.00501 25.3859C2.74013 25.6511 2.31061 25.6511 2.04517 25.3859L0.598406 23.9391C0.535351 23.8761 0.485329 23.8013 0.4512 23.719C0.417072 23.6366 0.399506 23.5483 0.399506 23.4592C0.399506 23.3701 0.417072 23.2818 0.4512 23.1995C0.485329 23.1171 0.535351 23.0423 0.598406 22.9793L16.2792 7.29845C16.3422 7.23533 16.417 7.18525 16.4994 7.15108C16.5817 7.11691 16.67 7.09932 16.7592 7.09932C16.8483 7.09932 16.9366 7.11691 17.019 7.15108C17.1013 7.18525 17.1761 7.23533 17.2391 7.29845ZM14.4231 13.2042L18.3792 9.24893L16.746 7.61541L12.7899 11.5713L14.4231 13.2042ZM17.4555 0.415771H16.7768V3.13037H17.4555V0.415771ZM17.4555 15.3462H16.7768V18.0608H17.4555V15.3462Z"
							fill="#CCCCCC"
						/>
					</svg>
				</button>
			</div>
		{:else if !ongoing_animation}
			<textarea
				data-testid="textbox"
				use:text_area_resize={value}
				class="scroll-hide"
				dir={rtl ? "rtl" : "ltr"}
				bind:value
				bind:this={el}
				{placeholder}
				rows={lines}
				{disabled}
				{autofocus}
				on:keypress={handle_keypress}
				on:blur
				on:select={handle_select}
				on:focus
				on:scroll={handle_scroll}
				style={text_align ? "text-align: " + text_align : ""}
			/>
		{/if}
	</div>
</label>

<style>
	label {
		display: block;
		width: 100%;
	}

	textarea {
		display: block;
		position: relative;
		outline: none !important;
		box-shadow: var(--input-shadow);
		background: var(--input-background-fill);
		padding: var(--input-padding);
		width: 100%;
		color: var(--body-text-color);
		font-weight: var(--input-text-weight);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		border: none;
	}
	label:not(.container),
	textarea:disabled {
		-webkit-text-fill-color: var(--body-text-color);
		-webkit-opacity: 1;
		opacity: 1;
	}

	textarea::placeholder {
		color: var(--input-placeholder-color);
	}
	.extend_button {
		display: flex;
		position: relative;
		align-items: center;
		width: 20px;
		height: 20px;
		overflow: hidden;
		color: var(--block-label-color);
		font: var(--font-sans);
		font-size: var(--button-small-text-size);
	}

	.extend_button:hover path {
		--ring-color: var(--color-accent);
		filter: brightness(1.1);
		fill: #ff6700;
	}

	.menu_section_prompt {
		padding: 12px 0px 0px 0px;
		align-items: center;
		color: #100700;
		font-family: Inter;
		font-size: 13px;
		font-style: normal;
		font-weight: 300;
		line-height: 24px;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 8px;
	}

	.menu_section_style {
		padding: 12px 0px 0px 0px;
		align-items: center;
		color: #100700;
		font-family: Inter;
		font-size: 13px;
		font-style: normal;
		font-weight: 300;
		line-height: 24px;
		display: flex;
		align-items: flex-start;
		flex-wrap: none;
		flex-direction: column;
		gap: 8px;
	}

	.menu_section_prompt ul {
		list-style-type: none;
		display: flex;
		align-items: flex-start;
		align-content: flex-start;
		gap: 4px 12px;
		flex-wrap: wrap;
		flex-direction: column;
		width: 100%;
	}

	.menu_section_style ul {
		list-style-type: none;
		display: flex;
		align-items: flex-start;
		align-content: flex-start;
		gap: 4px 12px;
		flex-wrap: wrap;
		flex-direction: row;
	}
	.menu_section_style li {
		width: auto;
	}

	.menu {
		border-radius: 0px 0px 15px 15px;
		background: rgba(204, 204, 204, 0.1);
		margin: 0px 16px;
		padding: 0px 14px 12px 14px;
	}

	.menu_section_prompt li {
		width: 100%;
	}

	.text_extension_button {
		border-radius: 15px;
		border: 0.5px solid #ff9a57;
		background: #fff4ea;
		cursor: pointer;
		display: flex;
		padding: 4px 12px;
		align-items: center;
		gap: 4px;
	}

	.text_extension_button_prompt {
		display: flex;
		width: 100%;
		padding: 8px 12px;
		justify-content: space-between;
		align-items: center;
		border-radius: 10px;
		border: 0.5px solid #ff9a57;
		background: #fff4ea;
		color: #101111;
		text-align: left;
		font-size: 13px;
		font-style: normal;
		font-weight: 300;
		line-height: normal;
		gap: 4px;
		flex-wrap: nowrap;
		flex-direction: row;
	}

	.text_extension_button_prompt:hover {
		color: #fff;
		fill: #fff;
		background: var(--Light-Orange, #ff9a57);
	}
	.text_extension_button_prompt:hover svg path {
		fill: #fff;
	}
	.text_extension_button:hover {
		color: #fff;
		background: var(--Light-Orange, #ff9a57);
	}
	.text_extension_button:hover svg path {
		fill: #fff;
	}

	.magic_container {
		display: flex;
		position: relative;
		outline: none !important;
		box-shadow: var(--input-shadow);
		padding: var(--input-padding);
		width: 100%;
		color: var(--body-text-color);
		font-weight: var(--input-text-weight);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		border: none;
		scrollbar-width: none;
		resize: none;
		align-items: center;
	}
</style>
