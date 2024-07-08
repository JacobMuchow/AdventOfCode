use md5;

pub fn md5_hash(str: &String) -> String {
    let digest = md5::compute(str);
    return format!("{:x}", digest);
}