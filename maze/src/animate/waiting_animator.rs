use super::Animator;

pub struct WaitingAnimator {
    frames_left: u32,
}

impl WaitingAnimator {
    pub fn new(frames: u32) -> Self {
        Self {
            frames_left: frames,
        }
    }
}

impl Animator for WaitingAnimator {
    fn update(&mut self) {
        self.frames_left = self.frames_left.saturating_sub(1);
    }

    fn draw(&self, _draw: &nannou::Draw, _window: &nannou::prelude::Rect) {}

    fn done(&self) -> bool {
        self.frames_left == 0
    }
}
