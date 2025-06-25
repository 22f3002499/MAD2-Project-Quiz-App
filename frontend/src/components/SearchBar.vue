<template>
  <BRow>
    <BCol cols="8">
      <BInputGroup size="lg">
        <BInputGroupText><i class="bi bi-search"></i></BInputGroupText>
        <BFormInput v-model="searchQuery" :placeholder="placeholder" />
      </BInputGroup>
    </BCol>

    <BCol v-if="sortByFields.length > 0">
      <BFormSelect
        v-model="selectedSortField"
        :options="sortByFieldOptions"
        size="lg"
      />
    </BCol>

    <BCol>
      <BFormSelect
        v-model="selectedSortOrder"
        :options="[
          { value: 'asc', text: 'Ascending' },
          { value: 'desc', text: 'Descending' },
        ]"
        size="lg"
      />
    </BCol>
  </BRow>

  <!-- Results -->
  <!-- <div> -->
  <!-- <slot :items="filteredAndSortedItems" :loading="false"> -->
  <!-- <div -->
  <!-- v-for="item in filteredAndSortedItems" -->
  <!-- :key="item.id || item" -->
  <!-- class="p-3 border rounded mb-2" -->
  <!-- > -->
  <!-- {{ typeof item === "object" ? JSON.stringify(item) : item }} -->
  <!-- </div> -->
  <!-- </slot> -->
  <!-- </div> -->
  <!-- </div> -->
</template>

<script setup>
import { ref, computed, watch } from "vue";

const props = defineProps({
  // Required
  items: {
    type: Array,
    required: true,
    default: () => [],
  },

  placeholder: {
    type: String,
    default: "Search...",
  },
  sortByFields: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["update"]);

// State
const searchQuery = ref("");
const selectedSortField = ref("");
const selectedSortOrder = ref("asc");

// Generate sort by field options
const sortByFieldOptions = computed(() => {
  if (props.sortByFields.length === 0) return [];

  return props.sortByFields.map((field) => ({
    value: field,
    text: field.charAt(0).toUpperCase() + field.slice(1), // Capitalize first letter
  }));
});

watch(
  () => props.sortByFields,
  (newFields) => {
    if (newFields.length > 0 && !selectedSortField.value) {
      selectedSortField.value = newFields[0];
    }
  },
  { immediate: true },
);

const filteredAndSortedItems = computed(() => {
  let result = [...props.items];

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    result = result.filter((item) => {
      // Convert entire object to searchable string
      const searchableText = getAllObjectValues(item).join(" ").toLowerCase();
      return searchableText.includes(query);
    });
  }

  // 2. Sort
  if (selectedSortField.value) {
    result.sort((a, b) => {
      const aValue = getValue(a, selectedSortField.value);
      const bValue = getValue(b, selectedSortField.value);

      // Handle different data types
      let comparison = 0;

      // Try to parse as numbers first
      const aNum = parseFloat(aValue);
      const bNum = parseFloat(bValue);

      if (!isNaN(aNum) && !isNaN(bNum)) {
        comparison = aNum - bNum;
      } else if (aValue instanceof Date && bValue instanceof Date) {
        comparison = aValue - bValue;
      } else {
        // String comparison
        comparison = aValue.toString().localeCompare(bValue.toString());
      }

      return selectedSortOrder.value === "desc" ? -comparison : comparison;
    });
  }

  return result;
});

// Helper function to get all values from an object (including nested)
const getAllObjectValues = (obj, values = []) => {
  if (obj === null || obj === undefined) return values;

  if (typeof obj === "object" && !Array.isArray(obj)) {
    Object.values(obj).forEach((value) => {
      if (typeof value === "object" && value !== null) {
        getAllObjectValues(value, values);
      } else if (value !== null && value !== undefined) {
        values.push(value.toString());
      }
    });
  } else if (Array.isArray(obj)) {
    obj.forEach((item) => getAllObjectValues(item, values));
  } else {
    values.push(obj.toString());
  }

  return values;
};

// Helper function to get nested values (e.g., 'user.name')
const getValue = (obj, path) => {
  if (typeof obj !== "object" || obj === null) return obj;
  return path.split(".").reduce((current, key) => current?.[key], obj);
};

// Emit changes
watch(
  filteredAndSortedItems,
  (newItems) => {
    emit("update", newItems);
  },
  { immediate: true },
);
</script>
