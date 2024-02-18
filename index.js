import { Flex, Box } from 'reflexbox';

export default function Home() {
  return (
    <Flex flexDirection="column" alignItems="center" justifyContent="center" height="100vh">
      <Box width={[1, 1/2, 1/4]} px={2}>
        <h1>Upload Sunscreen Image</h1>
        <form>
          <input type="file" accept="image/*" />
          <button type="submit">Upload</button>
        </form>
      </Box>
    </Flex>
  );
}