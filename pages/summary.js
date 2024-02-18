import { useRouter } from 'next/router';
import { Flex, Box } from 'reflexbox';

export default function Summary() {
  const router = useRouter();
  const { text } = router.query; // Get the extracted text from the query

  return (
    <Flex flexDirection="column" alignItems="center" justifyContent="center" height="100vh">
      <Box width={[1, 1/2, 1/4]} px={2}>
        <h1>Sunscreen Information</h1>
        <p>{text}</p> {/* Display the extracted text here */}
      </Box>
    </Flex>
  );
}
