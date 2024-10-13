self.current_position += self.current_velocity * 2.23694 * timestep
            self.commanded_authority -= self.current_velocity * 2.23694 * timestep
            self.commanded_authority_edit.setText(f"{self.commanded_authority:.2f} ft")