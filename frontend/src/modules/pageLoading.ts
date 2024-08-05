import { ref, computed } from 'vue';

// Create a reactive reference to keep track of the number of ongoing loading operations.
const loadingCount = ref(0);

// Create a computed property that returns true if there is at least one ongoing loading operation, otherwise false.
const isLoading = computed(() => loadingCount.value > 0);


/**
 * Updates the loading count based on the given value.
 * 
 * @param value - A boolean indicating whether to increment (true) or decrement (false) the loading count.
 */
export function setPageLoading(value: boolean) {
  if (value) {
    loadingCount.value++;
  } else {
    loadingCount.value--;
  }
}


/**
 * Provides access to the isLoading computed property.
 * 
 * @returns An object containing the isLoading computed property.
 */
export function usePageLoading() {
  return {
    isLoading
  };
}
