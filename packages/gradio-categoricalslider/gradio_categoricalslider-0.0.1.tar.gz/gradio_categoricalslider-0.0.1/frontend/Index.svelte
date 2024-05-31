<script context="module">
	let _id = 0;
</script>

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { Block, BlockTitle } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { afterUpdate } from "svelte";

	export let gradio: Gradio<{
		change: never;
		input: never;
		release: number;
		clear_status: LoadingStatus;
	}>;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: any = 0;
	export let label = gradio.i18n("slider.slider");
	export let info: string | undefined = undefined;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let show_label: boolean;
	export let interactive: boolean;
	export let loading_status: LoadingStatus;
	export let value_is_output = false;

	// New variable for categories using tuple structure
	export let categories: [string, any][] = [];

	let rangeInput: HTMLInputElement;

	const id = `range_id_${_id++}`;

	function handle_change(): void {
		gradio.dispatch("change");
		if (!value_is_output) {
			gradio.dispatch("input");
		}
	}

	afterUpdate(() => {
		value_is_output = false;
		setSlider();
	});

	function handle_release(e: MouseEvent): void {
		gradio.dispatch("release", value);
	}

	function setSlider(): void {
		setSliderRange();
		rangeInput.addEventListener("input", setSliderRange);
	}

	function setSliderRange(): void {
		const minValue = Math.min(...categories.map((cat) => cat[1]));
		const maxValue = Math.max(...categories.map((cat) => cat[1]));
		const dividend = Number(rangeInput.value) - minValue;
		const divisor = maxValue - minValue;
		const h = divisor === 0 ? 0 : dividend / divisor;
		rangeInput.style.backgroundSize = h * 100 + "% 100%";
	}

	$: disabled = !interactive;

	$: value, handle_change();
</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
	<StatusTracker
		autoscroll={gradio.autoscroll}
		i18n={gradio.i18n}
		{...loading_status}
		on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
	/>

	<div class="wrap">
		<div class="head">
			<label for={id}>
				<BlockTitle {show_label} {info}>{label}</BlockTitle>
			</label>
		</div>
		<div class="labels">
			{#each categories as [label, _]}
				<span>{label}</span>
			{/each}
		</div>
		<input
			type="range"
			{id}
			name="cowbell"
			bind:value
			bind:this={rangeInput}
			min={Math.min(...categories.map((cat) => cat[1]))}
			max={Math.max(...categories.map((cat) => cat[1]))}
			step={1}
			{disabled}
			on:pointerup={handle_release}
			aria-label={`range slider for ${label}`}
			class="slider"
		/>
	</div>
</Block>

<style>
	.wrap {
		display: flex;
		flex-direction: column;
		width: 100%;
	}

	.head {
		display: flex;
		justify-content: space-between;
	}

	input:disabled {
		-webkit-text-fill-color: var(--body-text-color);
		-webkit-opacity: 1;
		opacity: 1;
	}

	input::placeholder {
		color: var(--input-placeholder-color);
	}

	input[disabled] {
		cursor: not-allowed;
	}

	input[type="range"] {
		-webkit-appearance: none;
		appearance: none;
		width: 100%;
		accent-color: var(--slider-color);
		height: 4px;
		background: var(--neutral-200);
		border-radius: 5px;
		background-image: linear-gradient(
			var(--slider-color),
			var(--slider-color)
		);
		background-size: 0% 100%;
		background-repeat: no-repeat;
	}

	input[type="range"]::-webkit-slider-thumb {
		-webkit-appearance: none;
		box-shadow: var(--input-shadow);
		border: solid 0.5px #ddd;
		height: 20px;
		width: 20px;
		border-radius: 50%;
		background-color: white;
		cursor: pointer;
		margin-top: -2px;
		transition: background-color 0.1s ease;
	}

	input[type="range"]::-webkit-slider-thumb:hover {
		background: var(--neutral-50);
	}

	input[type="range"][disabled] {
		background: var(--body-text-color-subdued);
	}

	input[type="range"][disabled]::-webkit-slider-thumb {
		cursor: not-allowed;
		background-color: var(--body-text-color-subdued);
	}

	input[type="range"][disabled]::-moz-range-track {
		cursor: not-allowed;
		background-color: var(--body-text-color-subdued);
	}

	input[type="range"][disabled]::-webkit-slider-thumb:hover {
		background-color: var(--body-text-color-subdued);
	}

	input[type="range"][disabled]::-moz-range-track:hover {
		background-color: var(--body-text-color-subdued);
	}

	input[type="range"]::-webkit-slider-runnable-track {
		-webkit-appearance: none;
		box-shadow: none;
		border: none;
		background: transparent;
		height: 400%;
	}

	input[type="range"]::-moz-range-track {
		height: 12px;
	}

	.labels {
		margin-bottom: 10px;
		display: flex;
		justify-content: space-between;
		width: 100%;
		font-size: 14px;
		font-weight: 700;
		padding: 0 6px;
	}
</style>
