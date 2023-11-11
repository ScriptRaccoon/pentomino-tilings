export function memoize<S, T>(fn: (...args: S[]) => T) {
	const cache: Record<string, T> = {}
	return async function (...args: S[]) {
		if (args.toString() in cache) return cache[args.toString()]
		const result = await fn(...args)
		cache[args.toString()] = result
		return result
	}
}
