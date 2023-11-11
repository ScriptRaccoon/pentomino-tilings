<script lang="ts">
	import { onMount } from "svelte"
	import { COLORS, SIZES } from "./config"

	type coord = [number, number]
	type tiling = Record<string, Array<coord>>

	let tilings: Array<tiling>
	let names: Array<string>

	let current_index = 0
	$: current_tiling = tilings?.[current_index]

	let selected_height = "3"
	let n = 3
	let m = 20

	let loading = false

	async function init() {
		loading = true
		const new_n = parseInt(selected_height)
		const new_m = Math.floor(60 / new_n)
		const path = `/data/tilings-${new_n}-${new_m}.json`
		const res = await fetch(path)
		if (res.ok) {
			tilings = (await res.json()) as Array<tiling>
			current_index = 0
			n = new_n
			m = new_m
			if (!names) names = Object.keys(tilings[0] ?? {})
		} else {
			window.alert("Could not retrieve the data at this moment")
		}
		loading = false
	}

	function go_left() {
		current_index--
		if (current_index < 0) {
			current_index = tilings.length - 1
		}
	}

	function go_right() {
		current_index += 1
		if (current_index >= tilings.length) {
			current_index = 0
		}
	}

	onMount(init)
</script>

<header>
	<h1>Pentomino Tilings</h1>
</header>

<main>
	<menu>
		<div>
			<button
				disabled={!current_tiling}
				on:click={go_left}
				aria-label="previous"
			>
				<img
					src="arrow.svg"
					alt="arrow left"
					aria-hidden="true"
				/>
			</button>
			<button
				disabled={!current_tiling}
				on:click={go_right}
				aria-label="next"
			>
				<img
					class="flipped"
					src="arrow.svg"
					alt="arrow right"
					aria-hidden="true"
				/>
			</button>
		</div>

		<div>
			<label for="size">Size</label>
			<select
				id="size"
				bind:value={selected_height}
				on:change={init}
				disabled={loading}
			>
				{#each Object.entries(SIZES) as [value, label]}
					<option {value}>{@html label}</option>
				{/each}
			</select>
		</div>
	</menu>

	{#if current_tiling}
		<h2 class="counter" aria-live="polite">
			Tiling #{current_index + 1}
		</h2>
		<div class="board" style:--n={n} style:--m={m}>
			{#each names as name}
				{#each { length: 5 } as _, index}
					{@const [y, x] = current_tiling[name][index]}
					<div
						class="cell"
						style:--x={x}
						style:--y={y}
						style:--color={COLORS[name]}
					/>
				{/each}
			{/each}
		</div>
	{/if}

	{#if loading}
		<div>Loading...</div>
	{/if}
</main>

<style>
	header {
		padding-block: 2rem;
	}

	h1 {
		line-height: 1.1;
	}

	menu {
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}

	menu div {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.counter {
		font-size: 1.25rem;
		font-weight: initial;
		margin-block: 1rem 0.5rem;
	}

	.board {
		--u: min(5rem, calc((100vw - 2rem) / var(--m)));
		position: relative;
		height: calc(var(--n) * var(--u));
		width: calc(var(--m) * var(--u));
		margin-block: 0.5rem;
	}

	.cell {
		background-color: var(--color);
		width: var(--u);
		height: var(--u);
		left: calc(var(--x) * var(--u));
		top: calc(var(--y) * var(--u));
		border: 1px solid var(--bg);
		position: absolute;
		transition: 750ms ease;
	}

	button {
		opacity: 0.75;
	}

	button:hover,
	button:focus-visible {
		opacity: 1;
	}

	@media (min-width: 42rem) {
		h1 {
			font-size: 3rem;
		}
	}
</style>
