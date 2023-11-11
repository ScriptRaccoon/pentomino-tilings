import { memoize } from "./utils"

type coord = [number, number]
export type tiling = Record<string, Array<coord>>

export const get_tilings = memoize(get_tilings_from_json)

export async function get_tilings_from_json(
	n: number,
	m: number
): Promise<Array<tiling> | null> {
	const path = `/data/tilings-${n}-${m}.json`
	const res = await fetch(path)
	return res.ok ? ((await res.json()) as Array<tiling>) : null
}
