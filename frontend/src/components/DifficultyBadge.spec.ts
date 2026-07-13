import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import DifficultyBadge from './DifficultyBadge.vue'

describe('DifficultyBadge', () => {
  it('renders difficulty label', () => {
    const wrapper = mount(DifficultyBadge, { props: { difficulty: 'Easy' } })
    expect(wrapper.text()).toContain('Easy')
    expect(wrapper.classes()).toContain('badge-easy')
  })
})
