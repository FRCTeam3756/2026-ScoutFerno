import { create } from 'zustand'
import { devtools, persist, PersistOptions } from 'zustand/middleware'

type WithRequired<T, K extends keyof T> = T & { [P in K]-?: T[P] }

/**
 * Create a zustand store.
 * @param initialState The initial state of the store
 * @param name The name of the store
 * @param localStorageOptions Local storage will be used if provided.
 * @returns A store
 */
export function createStore<T extends object>(
  initialState: T,
  name: string,
  localStorageOptions?: WithRequired<Omit<PersistOptions<T>, 'name'>, 'version'>
) {
  if (localStorageOptions) {
    return create<T>()(
      devtools(
        persist(() => initialState, { ...localStorageOptions, name }),
        { name }
      )
    )
  }

  return create<T>()(devtools(() => initialState, { name }))
}
