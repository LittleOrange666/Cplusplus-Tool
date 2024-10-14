use std::io::{stdin};
type ll = i64;
type ld = f64;
const big: ll = 1e18 as ll;
struct Reader {
    buffer: Vec<String>,
}
impl Reader {
    fn new() -> Self {
        Reader { buffer: Vec::new() }
    }
    fn read_line(&self) -> String {
        let mut temp = String::new();
        stdin().read_line(&mut temp).unwrap();
        temp
    }
    fn read_token(&mut self) -> String {
        if self.buffer.is_empty() {
            self.buffer.extend(self.read_line().split(" ").map(|s| s.to_string()));
            self.buffer.reverse();
        }
        self.buffer.pop().unwrap()
    }
    pub fn read<T>(&mut self) -> T where T: std::str::FromStr {
        self.read_token().trim().parse::<T>().ok().unwrap()
    }
    pub fn reads<T>(&mut self, n: i32) -> Vec<T> where T: std::str::FromStr {
        (0..n).map(|_| self.read()).collect::<Vec<T>>()
    }
}
fn main() {
    let mut cin = Reader::new();
}